import { useState } from 'react';
import { Link } from 'react-router-dom';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';

const Sidebar = () => {
  const [hoverIndex, setHoverIndex] = useState<number | null>(null);

  const sidebarItems = [
    { path: '/', icon: <HomeIcon />, text: 'Home' },
    // Add additional items as needed
  ];

  return (
    <div className="sidebar" style={{ padding: '20px', backgroundColor: '#1976d2', height: '100%', color: 'white' }}>
      <List>
        {sidebarItems.map((item, index) => (
          <Link to={item.path} className="sidebar-link" key={index} style={{ textDecoration: 'none' }}>
            <ListItem
              style={{
                marginBottom: '10px',
                padding: '10px',
                backgroundColor: hoverIndex === index ? '#1e88e5' : '#1976d2',
                borderRadius: '4px',
                color: 'white',
              }}
              onMouseEnter={() => setHoverIndex(index)}
              onMouseLeave={() => setHoverIndex(null)}
            >
              <ListItemIcon style={{ minWidth: '40px', color: '#fff' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} style={{ color: '#fff', fontSize: '1rem' }}/>
            </ListItem>
          </Link>
        ))}
      </List>
    </div>
  );
};

export default Sidebar;