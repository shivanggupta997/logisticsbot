pipeline {
    agent any

    environment {
        IMAGE_NAME = "darksmiley1907/ailogibot"
        TAG = "latest"
    }

    stages {
        stage('Checkout') {
            steps {
                git branch: 'main', url: 'https://github.com/shivanggupta997/logisticsbot.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t $IMAGE_NAME:$TAG .'
            }
        }

        stage('Push to Docker Hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'dockerhub-creds', usernameVariable: 'DOCKER_USER', passwordVariable: 'DOCKER_PASS')]) {
                    sh '''
                        echo "$DOCKER_PASS" | docker login -u "$DOCKER_USER" --password-stdin
                        docker push $IMAGE_NAME:$TAG
                        docker logout
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes via Minikube') {
            steps {
                sh '''
                    export KUBECONFIG=$HOME/.kube/config
                    kubectl config use-context minikube
                    kubectl delete -f k8s/deployment.yaml --ignore-not-found
                    kubectl delete -f k8s/service.yaml --ignore-not-found
                    kubectl apply -f k8s/deployment.yaml
                    kubectl apply -f k8s/service.yaml
                    kubectl rollout status deployment/ailogibot
                    pkill -f 'kubectl port-forward' || true
                    nohup kubectl port-forward service/ailogibot 8000:80 > /tmp/portforward.log 2>&1 &
                '''
            }
        }
    }
}
