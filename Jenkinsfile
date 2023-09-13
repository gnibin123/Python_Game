pipeline {
  agent any
  stages {
    stage('Checkout') {
      steps {
        git(changelog: true, poll: true, url: 'https://github.com/gnibin123/Project_1.git', branch: 'main')
      }
    }

  }
}