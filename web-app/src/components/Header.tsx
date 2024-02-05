import AppBar from '@mui/material/AppBar';
import Toolbar from '@mui/material/Toolbar';
import InputBase from '@mui/material/InputBase';
import SearchIcon from '@mui/icons-material/Search';
import IconButton from '@mui/material/IconButton';
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import MoreVertIcon from '@mui/icons-material/MoreVert';
import { useEffect, useState } from 'react';

const Header = () => {
  const [currentTime, setCurrentTime] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => {
      clearInterval(timer);
    };
  }, []);

  return (
    <div style={{ width: '100%' }}>
      <AppBar position="sticky" style={{ width: '100%', backgroundColor: '#1976d2', color: 'white', display: 'flex', justifyContent: 'center', padding: '6px 10px', alignItems: 'center', minHeight: '64px' }}>
        <Toolbar style={{ justifyContent: 'space-between', width: '100%', padding: '0 20px', minHeight: '0px' }}>
          {/* Search Bar */}
          <div style={{ display: 'flex', alignItems: 'center', backgroundColor: 'white', borderRadius: '5px', padding: '4px 8px', marginRight: '20px', flexGrow: 1, marginLeft: '150px', maxWidth: '500px' }}>
            <SearchIcon style={{ color: '#1976d2', marginRight: '10px', width: '20px', height: '20px', marginLeft: '2px' }} />
            <InputBase
              placeholder="Search..."
              style={{ padding: '6px 0px', width: '100%', border: 'none', outline: 'none', fontSize: '1rem' }}
              inputProps={{ 'aria-label': 'search' }}
            />
          </div>

          {/* Icon Group */}
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '4px',
            padding: '0 16px',
            flex: 'none' // Prevents the div from growing or shrinking
          }}>
            <IconButton aria-label="help" color="inherit" style={{ padding: '8px' }}>
              <HelpOutlineIcon />
            </IconButton>
            <IconButton aria-label="account of current user" color="inherit" style={{ padding: '8px' }}>
              <AccountCircleIcon />
            </IconButton>
            <IconButton aria-label="display more actions" color="inherit" style={{ padding: '8px' }}>
              <MoreVertIcon />
            </IconButton>
            {/* Time Display */}
            <div style={{
              fontSize: '0.875rem',
              marginLeft: '16px',
              paddingLeft: '8px',
              paddingRight: '16px',
              whiteSpace: 'nowrap',
              flexShrink: 0 // Prevent the time display from shrinking
            }}>
              {currentTime.toLocaleTimeString()}
            </div>
          </div>
        </Toolbar>
      </AppBar>
    </div>
  );
};

export default Header;