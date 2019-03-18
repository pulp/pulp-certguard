#!/usr/bin/env bash
# coding=utf-8
set -veuo pipefail

# check the commit message
./.travis/check_commit.sh

# Lint code.
flake8 --config flake8.cfg || exit 1

# Run core migrations.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
export PULP_CONTENT_HOST=localhost:8080

# Make plugin migrations
pulp-manager makemigrations file --noinput
pulp-manager makemigrations certguard --noinput

# Run migrations
pulp-manager migrate --noinput


# Run unit tests.
(cd ../pulpcore && coverage run manage.py test pulp_certguard.tests.unit)

# Run functional tests.
export DJANGO_SETTINGS_MODULE=pulpcore.app.settings
pulp-manager reset-admin-password --password admin
pulp-manager runserver >> ~/django_runserver.log 2>&1 &
gunicorn pulpcore.content:server --bind 'localhost:8080' --worker-class 'aiohttp.GunicornWebWorker' -w 2 >> ~/content_app.log 2>&1 &
rq worker -n 'resource-manager@%h' -w 'pulpcore.tasking.worker.PulpWorker' >> ~/resource_manager.log 2>&1 &
rq worker -n 'reserved-resource-worker_1@%h' -w 'pulpcore.tasking.worker.PulpWorker' >> ~/reserved_worker-1.log 2>&1 &
sleep 8

show_logs_and_return_non_zero() {
    readonly local rc="$?"
    cat ~/django_runserver.log
    cat ~/content_app.log
    cat ~/resource_manager.log
    cat ~/reserved_worker-1.log
    return "${rc}"
}
pytest -v -r sx --color=yes --pyargs pulp_certguard.tests.functional || show_logs_and_return_non_zero

# Travis' scripts use unbound variables. This is problematic, because the
# changes made to this script's environment appear to persist when Travis'
# scripts execute. Perhaps this script is sourced by Travis? Regardless of why,
# we need to reset the environment when this script finishes.
#
# We can't use `trap cleanup_function EXIT` or similar, because this script is
# apparently sourced, and such a trap won't execute until the (buggy!) calling
# script finishes.
set +euo pipefail
