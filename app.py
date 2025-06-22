from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from datetime import datetime
import os
import logging
import random
from functools import wraps

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta_aqui_123456'  # Necessário para sessões e flash

# Usuários fixos para autenticação (substitua por um banco de dados em produção)
USERS = {
    'admin': 'senha123',
    'Rivaldo': 'manejo12'
}

def login_required(f):
    """Decorador para proteger rotas que exigem login."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash('Por favor, faça login para acessar esta página.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

class PlanoAulaGenerator:
    """Classe para gerar planos de aula personalizados."""
    
    DISCIPLINAS = ['História', 'Geografia', 'Português', 'Matemática', 'Biologia', 'Física', 'Química', 'Inglês', 'Educação Física']
    CLASSES = ['7ª Classe', '8ª Classe', '9ª Classe', '10ª Classe', '11ª Classe', '12ª Classe']
    DURACOES = [45, 90]
    FOCOS = ['Teórica', 'Prática/Experimental', 'Revisão', 'Avaliação', 'Introdução']

    def __init__(self):
        self.objetivos_base = {
            'Teórica': lambda tema: [
                f"Compreender os conceitos fundamentais de {tema}.",
                f"Analisar criticamente os aspectos principais de {tema}.",
                f"Relacionar {tema} com contextos históricos ou sociais."
            ],
            'Prática/Experimental': lambda tema: [
                f"Aplicar {tema} em exercícios práticos.",
                f"Desenvolver habilidades experimentais relacionadas a {tema}.",
                "Trabalhar em grupo para resolver problemas."
            ],
            'Revisão': lambda tema: [
                f"Revisar os principais pontos de {tema}.",
                f"Consolidar o aprendizado sobre {tema} com exercícios.",
                "Esclarecer dúvidas dos alunos."
            ],
            'Avaliação': lambda tema: [
                f"Avaliar o domínio de {tema} por meio de atividades.",
                f"Identificar lacunas no aprendizado sobre {tema}.",
                "Promover a autoavaliação."
            ],
            'Introdução': lambda tema: [
                f"Introduzir {tema} de forma envolvente.",
                f"Despertar curiosidade sobre {tema}.",
                f"Conectar {tema} ao cotidiano dos alunos."
            ]
        }

        self.conteudos_base = {
            'História': lambda tema: [
                f"Contexto histórico de {tema}.",
                "Eventos e figuras principais.",
                "Impactos e legados."
            ],
            'Geografia': lambda tema: [
                f"Aspectos geográficos de {tema}.",
                "Relações socioeconômicas.",
                "Análise de mapas ou dados."
            ],
            'Português': lambda tema: [
                f"Análise textual sobre {tema}.",
                "Estruturas linguísticas.",
                "Produção textual."
            ],
            'Matemática': lambda tema: [
                f"Conceitos matemáticos de {tema}.",
                "Resolução de problemas.",
                "Aplicações práticas."
            ]
        }

        self.tecnicas_ensino = {
            'Teórica': ['Exposição dialogada', 'Aula expositiva', 'Debate'],
            'Prática/Experimental': ['Resolução de problemas', 'Atividade prática', 'Simulação'],
            'Revisão': ['Revisão guiada', 'Exercícios de fixação', 'Discussão de dúvidas'],
            'Avaliação': ['Prova escrita', 'Apresentação oral', 'Autoavaliação'],
            'Introdução': ['Brainstorming', 'Estudo de caso', 'Vídeo introdutório']
        }

        self.meios_ensino = [
            'Quadro e marcador/giz',
            'Material impresso',
            'Projetor multimídia',
            'Livro didático',
            'Recursos digitais'
        ]

    def gerar_cronograma(self, duracao, tema, foco):
        """Gera o cronograma da aula em formato de tabela."""
        if duracao == 90:
            tempos = [10, 40, 30, 10]  # Proporcional para 90 minutos
        else:
            tempos = [5, 20, 15, 5]   # Padrão para 45 minutos

        cronograma = [
            {
                'tempo': f"{tempos[0]}'",
                'funcao': 'Introdução e Motivação',
                'conteudo': f"Apresentação de {tema}",
                'ativ_professor': f"Introduzir {tema} e contextualizar.",
                'ativ_aluno': 'Participar da discussão inicial.',
                'tecnica': self.tecnicas_ensino[foco][0],
                'meios': self.meios_ensino[0]
            },
            {
                'tempo': f"{tempos[1]}'",
                'funcao': 'Mediação e Assimilação',
                'conteudo': f"Exploração detalhada de {tema}",
                'ativ_professor': f"Explicar os conceitos principais de {tema}.",
                'ativ_aluno': 'Anotar e fazer perguntas.',
                'tecnica': self.tecnicas_ensino[foco][1],
                'meios': self.meios_ensino[1]
            },
            {
                'tempo': f"{tempos[2]}'",
                'funcao': 'Domínio e Consolidação',
                'conteudo': f"Aplicação prática de {tema}",
                'ativ_professor': f"Orientar atividades práticas sobre {tema}.",
                'ativ_aluno': 'Realizar exercícios ou projetos.',
                'tecnica': self.tecnicas_ensino[foco][2],
                'meios': self.meios_ensino[2]
            },
            {
                'tempo': f"{tempos[3]}'",
                'funcao': 'Controlo e Avaliação',
                'conteudo': f"Avaliação de {tema}",
                'ativ_professor': f"Avaliar o aprendizado sobre {tema}.",
                'ativ_aluno': 'Responder a questões ou apresentar resultados.',
                'tecnica': self.tecnicas_ensino[foco][0],
                'meios': self.meios_ensino[3]
            }
        ]
        return cronograma

    def gerar_atividades(self, tema, foco):
        """Gera atividades com base no foco da aula."""
        if foco == 'Prática/Experimental':
            return [
                f"Exercícios práticos sobre {tema}.",
                "Atividade experimental em grupo.",
                "Resolução de problemas colaborativa."
            ]
        return [
            f"Questionário sobre {tema}.",
            "Discussão dirigida.",
            f"Análise de materiais relacionados a {tema}."
        ]

    def criar_plano(self, tema, disciplina, classe, duracao, foco):
        """Gera o plano de aula completo."""
        try:
            data = datetime.now().strftime("%d/%m/%Y")
            objetivos = self.objetivos_base.get(foco, self.objetivos_base['Teórica'])(tema)
            conteudo = self.conteudos_base.get(disciplina, lambda t: [f"Introdução a {t}.", "Conceitos básicos.", "Exemplos."])(tema)
            cronograma = self.gerar_cronograma(duracao, tema, foco)
            atividades = self.gerar_atividades(tema, foco)

            # Formatar tabela do cronograma
            tabela = [
                "+--------+-------------------------+----------------------------+----------------------------+----------------------------+-------------------------+-------------------------+",
                "| Tempo  | Função Didática         | Conteúdo                   | Atividades (Professor)     | Atividades (Aluno)         | Técnica de Ensino       | Meios de Ensino         |",
                "+--------+-------------------------+----------------------------+----------------------------+----------------------------+-------------------------+-------------------------+"
            ]
            for linha in cronograma:
                tabela.append(
                    f"| {linha['tempo']:<6} | {linha['funcao']:<23} | {linha['conteudo']:<26} | {linha['ativ_professor']:<26} | {linha['ativ_aluno']:<26} | {linha['tecnica']:<23} | {linha['meios']:<23} |"
                )
            tabela.append("+--------+-------------------------+----------------------------+----------------------------+----------------------------+-------------------------+-------------------------+")
            tabela_cronograma = "\n".join(tabela)

            plano = f"""PLANO DE AULA

Escola: Escola Secundária
Data: {data}
Duração: {duracao} minutos
Disciplina: {disciplina}
Classe, Turma: {classe}, A
Unidade Temática: {tema}
Tema: {tema}

OBJETIVOS ESPECÍFICOS
{'\n'.join(f'- {obj}' for obj in objetivos)}

CONTEÚDO
{'\n'.join(f'- {item}' for item in conteudo)}

CRONOGRAMA
{tabela_cronograma}

RECURSOS DIDÁTICOS
{'\n'.join(f'- {meio}' for meio in self.meios_ensino[:3])}

ATIVIDADES
{'\n'.join(f'- {atividade}' for atividade in atividades)}

AVALIAÇÃO
- Participação nas atividades
- Compreensão do tema
- Colaboração em grupo

TAREFA DE CASA
- Leitura complementar sobre {tema}
- Exercícios de fixação
"""
            return plano
        except Exception as e:
            logger.error(f"Erro ao criar plano: {str(e)}")
            raise

# Instanciar o gerador
generator = PlanoAulaGenerator()

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Rota para login de usuários."""
    if 'user' in session:
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        logger.info(f"Tentativa de login: username='{username}'")
        
        if username in USERS and USERS[username] == password:
            session['user'] = username
            flash('Login realizado com sucesso!', 'success')
            logger.info(f"Login bem-sucedido: {username}")
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos.', 'error')
            logger.warning(f"Login falhou: username='{username}'")
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    """Rota para logout."""
    session.pop('user', None)
    flash('Você foi desconectado.', 'success')
    logger.info("Logout realizado")
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    """Renderiza o formulário principal."""
    return render_template('index.html',
                           disciplinas=generator.DISCIPLINAS,
                           classes=generator.CLASSES,
                           duracoes=generator.DURACOES,
                           focos=generator.FOCOS,
                           user=session['user'])

@app.route('/gerar', methods=['POST'])
@login_required
def gerar_plano():
    """Gera o plano de aula a partir do formulário."""
    try:
        # Obter dados do formulário
        tema = request.form.get('tema', '').strip()
        disciplina = request.form.get('disciplina', '').strip()
        classe = request.form.get('classe', '').strip()
        duracao = request.form.get('duracao', '').strip()
        foco = request.form.get('foco', '').strip()

        # Log para depuração
        logger.info(f"Dados recebidos: tema='{tema}', disciplina='{disciplina}', classe='{classe}', duracao='{duracao}', foco='{foco}'")

        # Validar campos
        if not all([tema, disciplina, classe, duracao, foco]):
            logger.warning("Campos obrigatórios faltando")
            return jsonify({'success': False, 'error': 'Todos os campos são obrigatórios'}), 400

        # Validar duração
        try:
            duracao = int(duracao)
            if duracao not in generator.DURACOES:
                raise ValueError("Duração inválida")
        except ValueError:
            logger.error("Duração inválida")
            return jsonify({'success': False, 'error': 'Duração deve ser 45 ou 90 minutos'}), 400

        # Validar outros campos
        if disciplina not in generator.DISCIPLINAS or classe not in generator.CLASSES or foco not in generator.FOCOS:
            logger.error("Valores inválidos para disciplina, classe ou foco")
            return jsonify({'success': False, 'error': 'Valores inválidos selecionados'}), 400

        # Gerar plano
        plano = generator.criar_plano(tema, disciplina, classe, duracao, foco)
        logger.info("Plano gerado com sucesso")
        return jsonify({'success': True, 'plano': plano})

    except Exception as e:
        logger.error(f"Erro ao gerar plano: {str(e)}")
        return jsonify({'success': False, 'error': f'Erro interno: {str(e)}'}), 500

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if not username or not password:
            flash('Preencha todos os campos.', 'error')
        elif username in USERS:
            flash('Usuário já existe.', 'error')
        else:
            USERS[username] = password
            flash('Cadastro realizado com sucesso! Faça login.', 'success')
            return redirect(url_for('login'))
    return render_template('cadastro.html')
if __name__ == '__main__':
    # Criar pasta templates
    os.makedirs('templates', exist_ok=True)

    # Gerar login.html
    login_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Gerador de Planos de Aula</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
            color: #1f2937;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        }
        h1 {
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 1.5rem;
            color: #1e3a8a;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.3rem;
            color: #374151;
        }
        input {
            width: 100%;
            padding: 0.6rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 1rem;
            background: #f9fafb;
            transition: border-color 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
        }
        button {
            background: #1e3a8a;
            color: white;
            padding: 0.8rem;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: background 0.2s;
        }
        button:hover {
            background: #1e40af;
        }
        .message {
            padding: 0.75rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            text-align: center;
        }
        .message.success {
            background: #d1fae5;
            color: #065f46;
        }
        .message.error {
            background: #fef2f2;
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Login</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST" action="{{ url_for('login') }}">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
            </div>
            <div class="form-group">
                <label for="password">Senha</label>
               <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
            </div>
            <button type="submit">Entrar</button>
        </form>
        <div style="text-align:center; margin-top:1rem;">
            <a href="{{ url_for('cadastro') }}">Não tem cadastro? Clique aqui</a>
        </div>
    </div>
</body>
</html>
"""
    with open('templates/login.html', 'w', encoding='utf-8') as f:
        f.write(login_html)

  # Gerar cadastro.html
    cadastro_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Cadastro - Gerador de Planos de Aula</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
            color: #1f2937;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            max-width: 400px;
            width: 100%;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        }
        h1 {
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 1.5rem;
            color: #1e3a8a;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.3rem;
            color: #374151;
        }
        input {
            width: 100%;
            padding: 0.6rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 1rem;
            background: #f9fafb;
            transition: border-color 0.2s;
        }
        input:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
        }
        button {
            background: #1e3a8a;
            color: white;
            padding: 0.8rem;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: background 0.2s;
        }
        button:hover {
            background: #1e40af;
        }
        .message {
            padding: 0.75rem;
            border-radius: 6px;
            margin-bottom: 1rem;
            text-align: center;
        }
        .message.success {
            background: #d1fae5;
            color: #065f46;
        }
        .message.error {
            background: #fef2f2;
            color: #dc3545;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Cadastro</h1>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}
                {% for category, message in messages %}
                    <div class="message {{ category }}">{{ message }}</div>
                {% endfor %}
            {% endif %}
        {% endwith %}
        <form method="POST" action="{{ url_for('cadastro') }}">
            <div class="form-group">
                <label for="username">Usuário</label>
                <input type="text" id="username" name="username" placeholder="Digite seu usuário" required>
            </div>
            <div class="form-group">
                <label for="password">Senha</label>
                <input type="password" id="password" name="password" placeholder="Digite sua senha" required>
            </div>
            <button type="submit">Cadastrar</button>
        </form>
        <div style="text-align:center; margin-top:1rem;">
            <a href="{{ url_for('login') }}">Já tem cadastro? Faça login</a>
        </div>
    </div>
</body>
</html>
"""
    with open('templates/cadastro.html', 'w', encoding='utf-8') as f:
        f.write(cadastro_html)

    # Gerar index.html
    index_html = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gerador de Planos de Aula</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            margin: 0;
            padding: 20px;
            color: #1f2937;
        }
        .container {
            background: white;
            border-radius: 12px;
            padding: 2rem;
            max-width: 600px;
            width: 100%;
            box-shadow: 0 10px 15px rgba(0, 0, 0, 0.2);
        }
        h1 {
            font-size: 1.8rem;
            text-align: center;
            margin-bottom: 1.5rem;
            color: #1e3a8a;
        }
        .user-info {
            text-align: right;
            margin-bottom: 1rem;
            font-size: 0.9rem;
        }
        .user-info a {
            color: #3b82f6;
            text-decoration: none;
        }
        .user-info a:hover {
            text-decoration: underline;
        }
        .form-group {
            margin-bottom: 1rem;
        }
        label {
            display: block;
            font-weight: 600;
            margin-bottom: 0.3rem;
            color: #374151;
        }
        input, select {
            width: 100%;
            padding: 0.6rem;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 1rem;
            background: #f9fafb;
            transition: border-color 0.2s;
        }
        input:focus, select:focus {
            outline: none;
            border-color: #3b82f6;
            box-shadow: 0 0 5px rgba(59, 130, 246, 0.5);
        }
        .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 1rem;
        }
        button {
            background: #1e3a8a;
            color: white;
            padding: 0.8rem;
            border: none;
            border-radius: 6px;
            font-size: 1rem;
            cursor: pointer;
            width: 100%;
            margin-top: 1rem;
            transition: background 0.2s;
        }
        button:hover {
            background: #1e40af;
        }
        .loading {
            display: none;
            text-align: center;
            margin: 1rem 0;
            flex-direction: column;
            align-items: center;
        }
        .spinner {
            border: 3px solid #e5e7eb;
            border-top: 3px solid #1e3a8a;
            border-radius: 50%;
            width: 24px;
            height: 24px;
            animation: spin 1s linear infinite;
            margin-bottom: 0.5rem;
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .error {
            background: #fef2f2;
            color: #dc3545;
            padding: 0.75rem;
            border-radius: 6px;
            margin: 1rem 0;
            display: none;
            text-align: center;
        }
        .resultado {
            display: none;
            margin-top: 1.5rem;
            padding: 1rem;
            background: #f3f4f6;
            border-radius: 8px;
        }
        .plano-content {
            white-space: pre-line;
            font-family: 'Courier New', monospace;
            background: white;
            padding: 1rem;
            border-radius: 6px;
            border: 1px solid #e5e7eb;
            overflow-x: auto;
        }
        .actions {
            display: flex;
            gap: 0.5rem;
            margin-top: 1rem;
        }
        .btn-secondary {
            background: #6b7280;
            padding: 0.5rem;
            font-size: 0.875rem;
            flex: 1;
        }
        .btn-secondary:hover {
            background: #4b5563;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="user-info">
            Bem-vindo, {{ user }}! <a href="{{ url_for('logout') }}">Sair</a>
        </div>
        <h1>Gerador de Planos de Aula</h1>
        <form id="plano-form">
            <div class="form-group">
                <label for="tema">Tema da Aula</label>
                <input type="text" id="tema" name="tema" placeholder="Ex.: Revolução Francesa" required>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="disciplina">Disciplina</label>
                    <select id="disciplina" name="disciplina" required>
                        <option value="">Selecione...</option>
                        {% for item in disciplinas %}
                            <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label for="classe">Classe</label>
                    <select id="classe" name="classe" required>
                        <option value="">Selecione...</option>
                        {% for item in classes %}
                            <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <div class="form-row">
                <div class="form-group">
                    <label for="duracao">Duração (min)</label>
                    <select id="duracao" name="duracao" required>
                        <option value="">Selecione...</option>
                        {% for item in duracoes %}
                            <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                </div>
                <div class="form-group">
                    <label for="foco">Foco da Aula</label>
                    <select id="foco" name="foco" required>
                        <option value="">Selecione...</option>
                        {% for item in focos %}
                            <option value="{{ item }}">{{ item }}</option>
                        {% endfor %}
                    </select>
                </div>
            </div>
            <button type="submit">Gerar Plano</button>
        </form>
        <div class="loading" id="loading">
            <div class="spinner"></div>
            <span>Gerando plano...</span>
        </div>
        <div class="error" id="error"></div>
        <div class="resultado" id="resultado">
            <h3>Plano Gerado</h3>
            <div class="plano-content" id="plano-content"></div>
            <div class="actions">
                <button class="btn-secondary" onclick="copyPlan()">Copiar</button>
                <button class="btn-secondary" onclick="printPlan()">Imprimir</button>
                <button class="btn-secondary" onclick="newPlan()">Gerar Novo Plano</button>
            </div>
        </div>
    </div>
    <script>
        const form = document.getElementById('plano-form');
        const loading = document.getElementById('loading');
        const errorDiv = document.getElementById('error');
        const resultado = document.getElementById('resultado');
        const planoContent = document.getElementById('plano-content');

        form.addEventListener('submit', (e) => {
            e.preventDefault();
            gerarPlano();
        });

        async function gerarPlano() {
            try {
                loading.style.display = 'flex';
                errorDiv.style.display = 'none';
                resultado.style.display = 'none';

                const formData = new FormData(form);
                const response = await fetch('/gerar', {
                    method: 'POST',
                    body: formData
                });

                const data = await response.json();
                loading.style.display = 'none';

                if (!data.success) {
                    errorDiv.textContent = data.error;
                    errorDiv.style.display = 'block';
                } else {
                    planoContent.textContent = data.plano;
                    resultado.style.display = 'block';
                    resultado.scrollIntoView({ behavior: 'smooth' });
                }
            } catch (err) {
                loading.style.display = 'none';
                errorDiv.textContent = `Erro: ${err.message}`;
                errorDiv.style.display = 'block';
            }
        }

        function copyPlan() {
            navigator.clipboard.writeText(planoContent.textContent)
                .then(() => alert('Plano copiado para a área de transferência!'))
                .catch(() => alert('Erro ao copiar o plano.'));
        }

        function printPlan() {
            const win = window.open('', '_blank');
            win.document.write(`<pre style="font-family: monospace; padding: 20px;">${planoContent.textContent}</pre>`);
            win.document.close();
            win.print();
        }

        function newPlan() {
            form.reset();
            resultado.style.display = 'none';
            errorDiv.style.display = 'none';
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
    </script>
</body>
</html>
"""
    with open('templates/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)

    logger.info("Servidor iniciando em http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)