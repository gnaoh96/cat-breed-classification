pipeline {
    agent any

    options{
        // Max number of build logs to keep and days to keep
        buildDiscarder(logRotator(numToKeepStr: '5', daysToKeepStr: '5'))
        // Enable timestamp at each job in the pipeline
        timestamps()
    }

    environment{
        registry = 'gnaoh96/cat-breed-prediction'
        registryCredential = 'dockerhub'
    }

    stages {
        stage('Build') {
            steps {
                script {
                    echo 'Building image for deployment..'
                    dockerImage = docker.build registry + ":0.0.$BUILD_NUMBER" 
                    echo 'Pushing image to dockerhub..'
                    docker.withRegistry( '', registryCredential ) {
                        dockerImage.push()
                        dockerImage.push('latest')
                    }
                }
            }
        }

        stage('Deploy to Google Kubernetes Engine') {
            agent {
                kubernetes {
                    containerTemplate {
                        name 'helm' // Name of the container to be used for helm upgrade
                        image 'gnaoh96/jenkins-k8s:latest' // The image containing helm
                    }
                }
            }
            steps {
                script {
                    steps
                    container('helm') {
                        echo "Ready to deploy new model version"
                        sh("helm upgrade --install  cbp --set image.repository=${registry} \
                        --set image.tag=0.0.${BUILD_NUMBER} ./helm-charts/model-serving --namespace model-serving")
                        echo "Deploy new model version sucessfully!"
                    }
                }
            }
        }
    }
}