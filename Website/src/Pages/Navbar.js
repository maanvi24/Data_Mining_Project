// NavBar.js
import React from 'react';
import { Link } from 'react-router-dom';

const NavBar = ({ activePage }) => {
  const styles = {
    navbar: {
      overflow: 'hidden',
      backgroundColor: '#333',
      position: 'fixed',
      top: 0,
      width: '100%',
      display: 'flex',
      justifyContent: 'space-between',
      alignItems: 'center',
    },
    navLinks: {
      display: 'flex',
      justifyContent: 'flex-end',
    },
    navLink: {
      color: 'white',
      padding: '14px 16px',
      textDecoration: 'none',
      marginLeft: '20px',
      transition: 'color 0.3s ease',
      fontSize: '18px',
    },
    navLinkActive: {
      fontSize: '22px',
      color: '#66ccff', // Highlight color for the active link
    },
    title: {
      color: 'white',
      padding: '14px 16px',
      fontSize: '27px',
    },
  };

  return (
    <div style={styles.navbar}>
      <div style={styles.title}>Stock Market Prediction</div>
      <div style={styles.navLinks}>
        <Link style={{ ...styles.navLink, ...(activePage === 'home' && styles.navLinkActive) }} to="/">Home</Link>
        <Link style={{ ...styles.navLink, ...(activePage === 'about' && styles.navLinkActive) }} to="/about">About</Link>
        <Link style={{ ...styles.navLink, ...(activePage === 'live-feed' && styles.navLinkActive) }} to="/live-feed">Live Feed</Link>
        <Link style={{ ...styles.navLink, ...(activePage === 'summary' && styles.navLinkActive) }} to="/summary">Summary</Link>
      </div>
    </div>
  );
};

export default NavBar;
