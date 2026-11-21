pipeline {
    agent any

    options {
        timestamps()
        disableConcurrentBuilds()
    }

    environment {
        AWS_REGION = 'ap-south-1'
        AWS_ACCOUNT_ID = '445942110343'
        ECR_REGISTRY = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
        IMAGE_TAG = 'latest'
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build and Push Images') {
            steps {
                withCredentials([usernamePassword(
                    credentialsId: 'aws-credentials',
                    usernameVariable: 'AWS_ACCESS_KEY_ID',
                    passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                )]) {
                    sh '''
                        set -eu
                        export AWS_DEFAULT_REGION="$AWS_REGION"
                        aws sts get-caller-identity
                        aws ecr get-login-password --region "$AWS_REGION" |
                          docker login --username AWS --password-stdin "$ECR_REGISTRY"

                        docker build -t "$ECR_REGISTRY/auth:$IMAGE_TAG" \
                          -f backend/authService/Dockerfile backend/authService
                        docker build -t "$ECR_REGISTRY/streaming:$IMAGE_TAG" \
                          -f backend/streamingService/Dockerfile backend
                        docker build -t "$ECR_REGISTRY/admin:$IMAGE_TAG" \
                          -f backend/adminService/Dockerfile backend
                        docker build -t "$ECR_REGISTRY/chat:$IMAGE_TAG" \
                          -f backend/chatService/Dockerfile backend
                        docker build -t "$ECR_REGISTRY/frontend:$IMAGE_TAG" frontend

                        for service in auth streaming admin chat frontend; do
                          aws ecr describe-repositories \
                            --repository-names "$service" \
                            --region "$AWS_REGION" >/dev/null
                          docker push "$ECR_REGISTRY/$service:$IMAGE_TAG"
                        done

                        docker logout "$ECR_REGISTRY"
                    '''
                }
            }
        }
    }
}
