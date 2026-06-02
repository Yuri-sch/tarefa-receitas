    pipeline {
    agent any

    stages {
        stage('Integração Contínua (CI)') {
            steps {
                echo 'Iniciando testes e validação de qualidade (Linter)...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    flake8 .
                    coverage run manage.py test receitas
                '''
            }
        }
        
        stage('Aprovar Deploy: Homologação') {
            steps {
                // Esta é a pausa manual exigida na sua avaliação
                input message: 'O código passou nos testes! Deseja fazer o Deploy em HOMOLOGAÇÃO (Porta 8001)?', ok: 'Fazer Deploy'
            }
        }

        stage('Deploy Homologação') {
            steps {
                echo 'Subindo ambiente de Homologação...'
                // Puxa as senhas do cofre do Jenkins de forma segura e injeta no .env
                withCredentials([usernamePassword(credentialsId: 'credenciais-gmail', passwordVariable: 'GMAIL_PASS', usernameVariable: 'GMAIL_USER')]) {
                    sh '''
                        cat <<EOF > .env
ENVIRONMENT=homolog
DB_NAME=homolog_db
DB_USER=admin_homolog
DB_PASSWORD=senha_homolog
EMAIL_HOST_USER=$GMAIL_USER
EMAIL_HOST_PASSWORD=$GMAIL_PASS
WEB_PORT=8001
DB_PORT=5433
EOF
                        docker-compose -p homolog down -v
                        docker-compose -p homolog up -d --build
                        sleep 5
                        docker-compose -p homolog exec -T web python insert_dados.py
                    '''
                }
            }
        }

        stage('Aprovar Deploy: Produção') {
            steps {
                // Segunda pausa manual antes de afetar o usuário final
                input message: 'A Homologação foi validada pela equipe! Deseja fazer o Deploy em PRODUÇÃO (Porta 8000)?', ok: 'Fazer Deploy'
            }
        }

        stage('Deploy Produção') {
            steps {
                echo 'Subindo ambiente de Produção...'
                withCredentials([usernamePassword(credentialsId: 'credenciais-gmail', passwordVariable: 'GMAIL_PASS', usernameVariable: 'GMAIL_USER')]) {
                    sh '''
                        cat <<EOF > .env
ENVIRONMENT=prod
DB_NAME=prod_db
DB_USER=admin_prod
DB_PASSWORD=senha_prod_real
EMAIL_HOST_USER=$GMAIL_USER
EMAIL_HOST_PASSWORD=$GMAIL_PASS
WEB_PORT=8000
DB_PORT=5432
EOF
                        docker-compose -p prod down -v
                        docker-compose -p prod up -d --build
                        sleep 5
                        docker-compose -p prod exec -T web python insert_dados.py
                    '''
                }
            }
        }
    }
}