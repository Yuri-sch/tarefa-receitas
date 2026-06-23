pipeline {
    agent any

    stages {
        stage('Integração') {
            steps {
                echo 'Iniciando testes e validação de qualidade...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                    flake8 .
                    coverage run manage.py test receitas
                '''
            }
        }
        
        stage('Aprovar Homologação') {
            steps {
                // Isso gera a pausa visual e cria o botão verde com o texto personalizado
                input message: 'O código passou no Ambiente de Integração! Criar ambiente de Homologação?', ok: 'Aprovar'
            }
        }

        stage('Homologação') {
            steps {
                echo 'Subindo ambiente de Homologação...'
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
                        rm -f db.sqlite3
                        docker-compose -p homolog down
                        docker-compose -p homolog up -d --build
                        sleep 5
                        docker-compose -p homolog exec -T web python manage.py migrate
                        docker-compose -p homolog exec -T web python insert_dados.py
                    '''
                }
            }
        }

        stage('Aprovar Produção') {
            steps {
                // Segunda pausa com botão antes de ir para produção
                input message: 'Ambiente de homologação criado com sucesso! Lançar para Produção?', ok: 'Aprovar'
            }
        }

        stage('Produção') {
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
DB_PORT=5434
EOF
                        rm -f db.sqlite3
                        docker-compose -p prod down
                        docker-compose -p prod up -d --build
                        sleep 5
                        docker-compose -p prod exec -T web python manage.py migrate
                        docker-compose -p prod exec -T web python insert_dados.py
                    '''
                }
            }
        }
    }
}