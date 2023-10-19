import React from 'react';
import ReactDOM from 'react-dom/client';

import './styles/fonts.css';
import './styles/index.css';

import App from './App';
import Router from './services/router/router'


const root = ReactDOM.createRoot(document.getElementById('root') as HTMLElement);

root.render(
    <React.StrictMode>
        <App />
        <Router />
    </React.StrictMode>
);
