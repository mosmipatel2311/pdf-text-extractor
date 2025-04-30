pipeline {
    agent any

    stages {
        stage('Install dependencies') {
            steps {
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run OCR Script') {
            steps {
                sh 'python src/pdf2image_convert_from_path.py src/Agro-14.pdf output/'
            }
        }
    }
}

