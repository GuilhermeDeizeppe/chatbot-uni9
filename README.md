# chatbot-uni9
Chatbot para aula de Aplicações em Inteligência Artificial, utilizando linguagem Python e as bibliotecas Rasa e spaCy.

# Como utilizar

Este projeto está sendo desenvolvido na versão 3.7.6 da linguagem Python.

Através da biblioteca Rasa, estamos criando um chatbot que seja capaz de consultar a previsão do tempo e retornar as informações para o usuário.

Utilizamos a biblioteca spaCy para reconhecimento da entidade LOC (local).


Para entender melhor o funcionamento do Rasa, recomendo a documentação oficial: https://rasa.com/docs/rasa/

Para pegar os conceitos básicos do Rasa na prática: https://www.youtube.com/playlist?list=PL75e0qA87dlEjGAc9j9v3a5h1mxI2Z9fi


# Treinando o bot

Toda vez que for feito alterações nos arquivos que o bot utiliza para se comunicar, será necessário treiná-lo novamente através do comando "rasa train".

Para abrir o ambiente interativo, onde você poderá treinar o bot, utilize o comando "rasa interactive".


OBS.: para usar o ambiente interativo, é necessário rodar primeiro o servidor de actions através do comando "rasa run actions".


# nlu.yml

O documento nlu.yml serve para aarmazenar todas as intents criadas para o bot.

Para entender melhor o que são intents, verificar documentação Rasa.


# stories.yml

Em stories.yml ficam todas as informações sobre treinamentos anteriores através do rasa interactive ou digitados a mão.

O bot utiliza as informações dentro do documento stories.yml para basear suas próximas interações com o usuário.

Esse documento serve como uma "receita" que o bot utiliza para tentar entender da melhor forma como atender o usuário.


# config.yml

Neste documento ficam todas as informações de pipeline e policies.

Para entender melhor, sugiro consultar a documentação oficial do Rasa.


# domain.yml

No domain.yml, ficam registras intents, entities, slots, responses, actions e forms do nosso bot.

Por ser um documento muito abrangente, sugiro olhar as documentações do Rasa antes de fazer alterações.


# rules.yml

Em rules.yml ficam as regras que nosso bot deverá seguir.

Ser cauteloso ao criar regras, uma vez que elas sempre deverão ser seguidas, sendo impossível criar flexibilização nas interações.

OBS.: ao utilizar o documento stories.yml, ser cauteloso para não quebrar nenhuma regra de interação do bot, pois isso poderá causar problemas ao executar o chatbot em uma próxima vez.
