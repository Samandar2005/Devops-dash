FROM node:22-alpine

WORKDIR /app

# Keshni tejash uchun avval package.json ko'chiriladi
COPY package.json ./
RUN npm install

# Qolgan kodni ko'chiramiz
COPY . .

# Vite porti
EXPOSE 5173

# Host (tashqi dunyo) ga ruxsat berish
CMD ["npm", "run", "dev", "--", "--host"]