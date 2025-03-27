pipeline {
    agent any

    environment {
        IMAGE_NAME = "movie_boxoffice_prediction"
        CONTAINER_NAME = "movie_boxoffice_container"
        PORT = "5000"
    }

    stages {
        stage('Clone Repository') {
            steps {
                git 'https://github.com/your-repo-url.git'  // Replace with your repo
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    sh "docker build -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                script {
                    sh "docker run -d -p ${PORT}:${PORT} --name ${CONTAINER_NAME} ${IMAGE_NAME}:latest"
                }
            }
        }

        stage('Test Application') {
            steps {
                script {
                    sh "curl -I http://127.0.0.1:${PORT}"
                }
            }
        }

        stage('Cleanup') {
            steps {
                script {
                    sh "docker stop ${CONTAINER_NAME} || true"
                    sh "docker rm ${CONTAINER_NAME} || true"
                }
            }
        }
    }
}
