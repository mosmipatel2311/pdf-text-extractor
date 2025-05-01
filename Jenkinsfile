pipeline {
    agent any

    environment {
        SCRIPT_DIR = "C:/Users/Admin/Documents/workspace/agri-uni-pdf-convertor"
        PDF_PATH = "${SCRIPT_DIR}/AgroTechnologies2018-mini.pdf"
        OUTPUT_PATH = "${SCRIPT_DIR}/output_agrotechmdfiles_mini"
        TESSERACT_PATH = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    }

    stages {
        stage('Install Python Dependencies') {
            steps {
                bat '''
                cd %SCRIPT_DIR%
                python -m venv venv
                venv\\Scripts\\activate
                pip install -r requirements.txt
                '''
            }
        }

        stage('Run OCR Script') {
            steps {
                bat '''
                cd %SCRIPT_DIR%
                venv\\Scripts\\activate
                python src\\pdf2image_convert_from_path.py
                '''
            }
        }

        stage('Validate Output') {
            steps {
                bat '''
                if not exist "%OUTPUT_PATH%\\markdown\\page_1.md" (
                    echo Error: Markdown output not found!
                    exit /b 1
                )
                echo Output exists. QA Check passed.
                '''
            }
        }
    }

    post {
        success {
            echo '✅ QA pipeline passed.'
        }
        failure {
            echo '❌ QA pipeline failed.'
        }
    }
}


