// Define a Jenkins pipeline
pipeline {
    // Agent specifies where the pipeline will run.
    // 'any' means it can run on any available agent.
    // Ensure your Jenkins agent has git, docker, kubectl, and minikube installed.
    agent any

    // Stages define the steps of your pipeline
    stages {
        // Stage 1: Checkout SCM (Source Code Management)
        stage('Checkout Code') {
            steps {
                cleanWs() // Clean workspace before cloning
                git url: 'https://github.com/shivanggupta997/logisticsbot.git'
            }
        }

        // Stage 2: Build and Push Docker Image
        stage('Build & Push Docker Image') {
            steps {
                script {
                    def dockerImageName = 'darksmiley1907/ailogibot'
                    sh "docker build -t ${dockerImageName}:${BUILD_NUMBER} ."
                    sh "docker tag ${dockerImageName}:${BUILD_NUMBER} ${dockerImageName}:latest"

                    withDockerRegistry(credentialsId: 'dockerhub-credentials', url: 'https://index.docker.io/v1/') {
                        sh "docker push ${dockerImageName}:${BUILD_NUMBER}"
                        sh "docker push ${dockerImageName}:latest"
                    }
                }
            }
        }

        // Stage 3: Deploy to Minikube
        stage('Deploy to Minikube') {
            steps {
                script {
                    def dockerImageName = 'darksmiley1907/ailogibot'
                    def k8sDeploymentFile = 'deployment.yaml'
                    def k8sServiceFile = 'service.yaml'
                    def replicas = '3'
                    def dockerHubImage = 'ailogibot' // Used for kubectl delete and rollout status

                    // Clean up old resources
                    sh "kubectl delete deployment ${dockerHubImage} --ignore-not-found=true"
                    sh "kubectl delete service ${dockerHubImage}-service --ignore-not-found=true"

                    // Update deployment.yaml with new image and replica count
                    sh "sed -i 's|image:.*|image: ${dockerImageName}:${BUILD_NUMBER}|g' ${k8sDeploymentFile}"
                    sh "sed -i 's|replicas:.*|replicas: ${replicas}|g' ${k8sDeploymentFile}"

                    // Apply Kubernetes service and deployment files
                    sh "kubectl apply -f ${k8sServiceFile}"
                    sh "kubectl apply -f ${k8sDeploymentFile}"

                    // Wait for deployment to be ready
                    sh "kubectl rollout status deployment/${dockerHubImage}"
                }
            }
        }

        // Stage 4: Access Application
        stage('Access Application') {
            steps {
                script {
                    def dockerHubImage = 'ailogibot'
                    def serviceUrl = sh(returnStdout: true, script: "minikube service ${dockerHubImage}-service --url").trim()
                    echo "Application is accessible at: ${serviceUrl}"
                }
            }
        }
    }

    // Post-build actions (e.g., clean up workspace)
    post {
        always {
            cleanWs() // Clean up the workspace after the build
        }
    }
}
