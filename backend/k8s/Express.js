app.use(cors({
  origin: ['http://localhost:3000', 'http://frontend:3000'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));