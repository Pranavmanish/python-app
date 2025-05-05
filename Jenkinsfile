pipeline {
    agent any

    environment {
        DOCKER_IMAGE_BASE = 'pranav1706/python-app'  
        K8S_NAMESPACE = 'default'
    }

    stages {
        stage('Checkout') {
            steps {
                git credentialsId: 'Github-cred', branch: 'main', url: 'https://github.com/Pranavmanish/python-app.git'
            }
        }

        stage('Build & Test Flask App') {
            steps {
                script {
                    sh '''
                        echo "[*] Setting up virtual environment..."
                        python3 -m venv venv
                        . venv/bin/activate
                        pip install --upgrade pip
                        pip install -r requirements.txt

                        echo "[*] Running Flask app (test)..."
                        python run.py &
                        APP_PID=$!
                        sleep 10
                        kill $APP_PID || true
                    '''
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    def imageTag = "${DOCKER_IMAGE_BASE}:${env.BUILD_NUMBER}"
                    def latestTag = "${DOCKER_IMAGE_BASE}:latest"

                    sh """
                        echo "[*] Building Docker image..."
                        sudo docker build -t ${imageTag} .
                        sudo docker tag ${imageTag} ${latestTag}
                    """

                    env.DOCKER_IMAGE = imageTag
                }
            }
        }

        stage('Push Docker Image to DockerHub') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'Dockerhub-cred', usernameVariable: 'DOCKER_USERNAME', passwordVariable: 'DOCKER_PASSWORD')]) {
                        sh '''
                            echo "[*] Authenticating with DockerHub..."
                            sudo docker logout || true
                            echo $DOCKER_PASSWORD | sudo docker login -u $DOCKER_USERNAME --password-stdin

                            echo "[*] Pushing Docker image..."
                            sudo docker push ${DOCKER_IMAGE}
                            sudo docker push ${DOCKER_IMAGE_BASE}:latest
                        '''
                    }
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh '''
                            kubectl --kubeconfig=$KUBECONFIG apply -f deployment.yaml --namespace=$K8S_NAMESPACE
                            kubectl --kubeconfig=$KUBECONFIG apply -f service.yaml --namespace=$K8S_NAMESPACE
                        '''
                    }
                }
            }
        }

        stage('Update Deployment with New Docker Image') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        // Ensure deployment name matches the one in deployment.yaml
                        sh """
                            kubectl --kubeconfig=$KUBECONFIG set image deployment/python-app python-app-container=${env.DOCKER_IMAGE} --namespace=$K8S_NAMESPACE
                            kubectl --kubeconfig=$KUBECONFIG rollout status deployment/python-app --namespace=$K8S_NAMESPACE
                        """
                    }
                }
            }
        }
    }

    post {
        success {
            echo '✅ Python Survey App Deployed Successfully!'
        }
        failure {
            echo '❌ Deployment Failed.'
        }
    }
}
