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
                        docker build -t ${imageTag} .
                        docker tag ${imageTag} ${latestTag}
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
                            docker logout || true
                            echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin

                            echo "[*] Pushing Docker image..."
                            docker push ${DOCKER_IMAGE}
                            docker push ${DOCKER_IMAGE_BASE}:latest
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
                            echo "[*] Applying Kubernetes manifests..."
                            kubectl --kubeconfig=$KUBECONFIG apply -f deployment.yaml --namespace=$K8S_NAMESPACE --validate=false
                            kubectl --kubeconfig=$KUBECONFIG apply -f service.yaml --namespace=$K8S_NAMESPACE --validate=false
                            echo "[*] Waiting for deployment to be ready..."
                            kubectl --kubeconfig=$KUBECONFIG rollout status deployment/python-app --namespace=$K8S_NAMESPACE 
                        '''
                    }
                }
            }
        }

        stage('Update Deployment with New Docker Image') {
            steps {
                script {
                    withCredentials([file(credentialsId: 'kubeconfig', variable: 'KUBECONFIG')]) {
                        sh """
                            echo "[*] Updating container image in deployment..."
                            kubectl --kubeconfig=$KUBECONFIG set image deployment/mpython-app my-python-app-container=${env.DOCKER_IMAGE} --namespace=$K8S_NAMESPACE
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
