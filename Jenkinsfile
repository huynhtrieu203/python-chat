#!/usr/bin/env groovy

pipeline {
    agent any

    environment {
        AWS_ACCOUNT_ID="817735295857"
        AWS_DEFAULT_REGION="ap-southeast-1"
        IMAGE_REPO_NAME="project"
        REPOSITORY_URI = "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}"
        AWS_ECR_REGION = 'ap-southeast-1'
        DEPLOYMENT_URL_A = 'ec2-52-221-186-52.ap-southeast-1.compute.amazonaws.com'
        DEPLOYMENT_URL_B = 'ec2-13-251-103-157.ap-southeast-1.compute.amazonaws.com'
        SSH_USER = 'ec2-user'
    }

    stages {
        // Building Docker images
        stage('Building image') {
            steps{
                // withAWS(credentials: 'aws-access-credential') {
                script {
                    // def login = ecrLogin()
                    // sh('#!/bin/sh -e\n' + "${login}") // hide logging
                    sh '''
                        git fetch --tags --all
                        bash tag_count.sh
                        IMAGE_TAG=$(git tag --sort=-committerdate | head -n 1)
                        docker build -t $IMAGE_REPO_NAME:$IMAGE_TAG .
                    '''
                }
                // }
            }
        }

        //test
        stage('Testing') {
            steps{
                script {
                    sh'''
                        IMAGE_TAG=$(git tag --sort=-committerdate | head -n 1)
                        docker rm -f chatapp
                        docker run -d --rm --name chatapp "${IMAGE_REPO_NAME}:${IMAGE_TAG}"
                        sleep 10
                        docker ps
                    '''
                }
            }
        }

        // Uploading Docker images into AWS ECR
        stage('Pushing to ECR') {
            steps{
                withAWS(credentials: 'aws-access-credential') {
                    script {
                        def login = ecrLogin()
                        sh('#!/bin/sh -e\n' + "${login}") // hide logging
                        if (env.BRANCH_NAME.startsWith('release/')){
                            sh '''
                            IMAGE_TAG=$(git tag --sort=-committerdate | head -n 1)
                            docker tag ${IMAGE_REPO_NAME}:${IMAGE_TAG} ${REPOSITORY_URI}:${IMAGE_TAG}
                            docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_DEFAULT_REGION}.amazonaws.com/${IMAGE_REPO_NAME}:${IMAGE_TAG}
                            '''
                        }
                    }
                }
            }
        }

        // Updating auto.sh script
        stage('Update script'){
            steps{
                sh'''
                IMAGE_TAG=$(git tag --sort=-committerdate | head -n 1)
                cat <<EOT >> auto.sh
                docker pull 817735295857.dkr.ecr.ap-southeast-1.amazonaws.com/project:${IMAGE_TAG}
                docker run -d --name=chat-app -p 3000:5000 817735295857.dkr.ecr.ap-southeast-1.amazonaws.com/project:${IMAGE_TAG}
                EOT
                '''
            }
        }
        // Deploying image to EC2
        stage('Deploy in EC2') {
            steps {
                script {
                    if (env.BRANCH_NAME.startsWith('release/')){
                        sshagent(credentials : ['ssh']) {
                                sh '''
                                    chmod +x auto.sh
                                    // The 1st instance
                                    ssh -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOYMENT_URL_A} uptime
                                    ssh -v ${SSH_USER}@${DEPLOYMENT_URL_A} < ./auto.sh
                                    // The 2nd instance
                                    ssh -o StrictHostKeyChecking=no ${SSH_USER}@${DEPLOYMENT_URL_B} uptime
                                    ssh -v ${SSH_USER}@${DEPLOYMENT_URL_B} < ./auto.sh
                                '''
                        }
                    }
                }
            }
        }
    }

    post{
        always {
            script {
                    mail to: "vietlt215@gmail.com",
                    subject: "Report",
                    body: "Build result for ${env.BRANCH_NAME}: ${currentBuild.currentResult}"
            }       
        }
    }
}
