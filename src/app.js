/**
 * BisnisMate Express Application
 * Configures Middlewares, REST Endpoints, and Static Frontend
 */

const express = require('express');
const cors = require('cors');
const path = require('path');
const apiRoutes = require('./routes/api.routes');

const app = express();

// Security & Parsing Middlewares
app.use(cors());
app.use(express.json({ limit: '20mb' }));
app.use(express.urlencoded({ extended: true, limit: '20mb' }));

// Static Assets Hosting (Public folder)
const publicDir = path.join(__dirname, '../public');
app.use(express.static(publicDir));
app.use('/public', express.static(publicDir));
app.use('/assets', express.static(path.join(publicDir, 'assets')));

// Mount REST API
app.use('/api/v1', apiRoutes);

// Dedicated Motion Graphic Route (Argon 4)
app.get(['/video', '/motion-graphic', '/showreel'], (req, res) => {
  res.sendFile(path.join(publicDir, 'video.html'));
});

// SPA Single-Page-Application Fallback
app.use((req, res, next) => {
  if (req.method === 'GET' && !req.path.startsWith('/api/')) {
    return res.sendFile(path.join(publicDir, 'index.html'));
  }
  next();
});

// Centralized Error Handling Middleware
app.use((err, req, res, next) => {
  console.error('[SERVER ERROR]', err);
  res.status(500).json({
    status: 'error',
    message: err.message || 'Internal Server Error'
  });
});

module.exports = app;
