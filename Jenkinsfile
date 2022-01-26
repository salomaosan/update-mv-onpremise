pipeline {
    agent any
    environment {
        QUALITOR_SERVER=credentials('qualitor-server')
        QUALITOR_DATABASE=credentials('qualitor-database')
        QUALITOR_CREDENTIALS=credentials('qualitor-credentials')
        ZBX_URL=credentials('zbx-url')
        ZBX_CREDENTIALS=credentials('zabbix-credentials')
        ZBX_GROUPID=credentials('zbx-groupid')
    }
    stages {
        stage('Build') {
            steps{
                sh ('docker build -t my-python-app .')
            }
        }
        stage('Update') {
            steps{
                sh ('docker run --rm --env QUALITOR_SERVER=$QUALITOR_SERVER \
                --env QUALITOR_DATABASE=$QUALITOR_DATABASE \
                --env QUALITOR_USER=$QUALITOR_CREDENTIALS_USR \
                --env QUALITOR_PASS=$QUALITOR_CREDENTIALS_PSW \
                --env ZBX_URL=$ZBX_URL \
                --env ZBX_USER=$ZBX_CREDENTIALS_USR \
                --env ZBX_PASS=$ZBX_CREDENTIALS_PSW \
                --env ZBX_GROUPID=$ZBX_GROUPID \
                --name my-running-app my-python-app')
            }
        }
    }
}