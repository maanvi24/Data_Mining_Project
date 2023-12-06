// src/App.js
import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import NavBar from './Pages/Navbar';
import Home from './Pages/ArticleForm';
import About from './Pages/About';
import LiveFeed from './Pages/LiveFeed';
import Summary from './Pages/Summary';


function App() {
  return (
    <Router>
      <div className="App">
        <NavBar />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/live-feed" element={<LiveFeed />} />
          <Route path="/summary" element={<Summary />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

