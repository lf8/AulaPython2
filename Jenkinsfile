pipeline {
  agent any
  stages {
    stage('build') {
      steps {
        sh 'Echo \'Build\''
      }
    }
    stage('stage') {
      steps {
        sh 'echo \'stage\''
      }
    }
    stage('aprove') {
      steps {
        input 'Voce quer aprovar?'
      }
    }
  }
}