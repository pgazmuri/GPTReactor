import { Link } from 'react-router-dom';
import List from '@mui/material/List';
import ListItem from '@mui/material/ListItem';
import ListItemIcon from '@mui/material/ListItemIcon';
import ListItemText from '@mui/material/ListItemText';
import HomeIcon from '@mui/icons-material/Home';

const Sidebar = () => {
  const sidebarItems = [
    { path: '/', icon: <HomeIcon />, text: 'Home' },
    // Add additional items as needed
  ];

  return (
    <div className="sidebar">
      <List>
        {sidebarItems.map((item, index) => (
          <Link to={item.path} className="sidebar-link" key={index}>
            <ListItem>
              <ListItemIcon style={{ minWidth: '40px' }}>{item.icon}</ListItemIcon>
              <ListItemText primary={item.text} style={{ fontSize: '.5rem !important' }}/>
            </ListItem>
          </Link>
        ))}
      </List>
    </div>
  );
};

export default Sidebar;