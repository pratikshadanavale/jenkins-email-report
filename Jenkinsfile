pipeline {
    agent any

    tools {
        python 'Python3.12'  // Only if you set this in Jenkins. Otherwise, use full path below.
    }

    stages {
        stage('Checkout from GitHub') {
            steps {
                git credentialsId: 'github-creds-pratiksha', url: 'https://github.com/pratikshadanavale/jenkins-email-report.git'
            }
        }

        stage('Run Email Report Script') {
            steps {
                bat '''
                    python --version
                    python send_report.py
                '''
            }
        }
    }

    post {
        success {
            echo '✅ Build completed successfully.'
        }
        failure {
            echo '❌ Build failed.'
        }
    }
}
