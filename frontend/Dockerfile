# FROM node:20-slim

# WORKDIR /app

# COPY package*.json ./

# # --max-old-space-size limita o uso de memória do Node durante o install.
# # --prefer-offline usa cache quando possível.
# # Sem isso o Pi trava tentando compilar dependências nativas em ARM.
# RUN NODE_OPTIONS="--max-old-space-size=512" npm install --prefer-offline

# COPY . .

# # Build de produção também com memória limitada
# RUN NODE_OPTIONS="--max-old-space-size=512" npm run build

# EXPOSE 3000

# CMD ["npm", "start"]

FROM node:20-slim

WORKDIR /app

# Copia as dependências e o resultado do build feito localmente.
# Não rodamos npm install nem npm run build aqui — o Pi não tem RAM para isso.
# O build foi feito na máquina de desenvolvimento e o resultado é copiado pronto.
COPY package*.json ./
COPY .next/ ./.next/
#COPY public/ ./public/
COPY node_modules/ ./node_modules/

EXPOSE 3000

CMD ["npm", "start"]