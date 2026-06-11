pipeline {
    agent any

    // Aqui criamos o "Menu" inicial com caixas de seleção
    parameters {
        booleanParam(name: 'RUN_CI', defaultValue: true, description: '1. Rodar Testes e Validação de Código (CI)?')
        booleanParam(name: 'DEPLOY_HOMOLOG', defaultValue: false, description: '2. Fazer Deploy no Ambiente de HOMOLOGAÇÃO (Porta 8001)?')
        booleanParam(name: 'DEPLOY_PROD', defaultValue: false, description: '3. Fazer Deploy no Ambiente de PRODUÇÃO (Porta 8000)?')
    }

    stages {
        stage('Integração Contínua (CI)') {
            // Só roda se a caixa RUN_CI estiver marcada
            when { expression { params.RUN_CI } }
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
        
        stage('Deploy Homologação') {
            // Só roda se a caixa DEPLOY_HOMOLOG estiver marcada
            when { expression { params.DEPLOY_HOMOLOG } }
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
                        docker-compose -p homolog down -v
                        docker-compose -p homolog up -d --build
                        sleep 5
                        docker-compose -p homolog exec -T web python manage.py migrate
                        docker-compose -p homolog exec -T web python insert_dados.py
                    '''
                }
            }
        }

        stage('Deploy Produção') {
            // Só roda se a caixa DEPLOY_PROD estiver marcada
            when { expression { params.DEPLOY_PROD } }
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
                        docker-compose -p prod exec -T web python manage.py migrate
                        docker-compose -p prod exec -T web python insert_dados.py
                    '''
                }
            }
        }
    }
}