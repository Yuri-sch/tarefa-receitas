pipeline {
    agent any

    stages {
        stage('Preparação do Ambiente') {
            steps {
                echo 'Criando ambiente virtual e instalando dependências...'
                sh '''
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install --no-cache-dir -r requirements.txt
                '''
            }
        }
        stage('Análise de Qualidade (Flake8)') {
            steps {
                echo 'Rodando o Linter para verificar padrões PEP-8...'
                sh '''
                    . venv/bin/activate
                    flake8 .
                '''
            }
        }
        stage('Testes Automatizados e Cobertura') {
            steps {
                echo 'Rodando os 20 testes e gerando estatísticas...'
                // Como não passamos a variável ENVIRONMENT, ele usa o SQLite local,
                // que é o cenário perfeito e isolado para testes unitários em CI.
                sh '''
                    . venv/bin/activate
                    coverage run manage.py test receitas
                    coverage report
                '''
            }
        }
    }
}