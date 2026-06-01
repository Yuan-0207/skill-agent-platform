pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '20'))
    }

    environment {
        PYTHON = 'python'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend') {
            steps {
                script {
                    if (isUnix()) {
                        sh '''
                            python -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
                            PYTHONPATH=. python -m pytest backend/tests -q --junitxml=backend/tests-results.xml
                        '''
                    } else {
                        bat '''
                            python -m pip install -r backend/requirements.txt -r backend/requirements-dev.txt
                            set PYTHONPATH=%CD%
                            python -m pytest backend/tests -q --junitxml=backend/tests-results.xml
                        '''
                    }
                }
            }
        }

        stage('Frontend') {
            steps {
                dir('frontend') {
                    script {
                        if (isUnix()) {
                            sh 'npm install && npm run build'
                        } else {
                            bat 'npm install && npm run build'
                        }
                    }
                }
            }
        }
    }

    post {
        success {
            archiveArtifacts artifacts: 'frontend/dist/**/*', fingerprint: true
        }
        always {
            junit testResults: 'backend/tests-results.xml', allowEmptyResults: true
        }
    }
}
