node {
   stage('Get Source') {
      // copy source code from local file system and test
      // for a Dockerfile to build the Docker image
      git ('https://github.com/teamdws/document_mcs.git')
      if (!fileExists("Dockerfile")) {
         error('Dockerfile missing.')
      }
   }
   stage('Build Docker') {
       // build the docker image from the source code using the BUILD_ID parameter in image name
         sh "docker build --tag python-docker ."
   }
   stage("run docker container"){
        sh "docker run -d -p 5000:5000 python-docker "
    }
}
