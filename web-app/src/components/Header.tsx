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
    <AppBar position="static" style={{ width: '100%', backgroundColor: '#1976d2', color: 'white', display: 'flex', justifyContent: 'center', padding: '4px 8px', alignItems: 'center' }}>
      <Toolbar style={{ justifyContent: 'space-between', width: '100%', padding: '0', marginRight: '40px', paddingRight: '8px', minHeight: '0px' }}>
        {/* Search Bar */}
        <div style={{ display: 'flex', alignItems: 'center', backgroundColor: 'white', borderRadius: '5px', padding: '0px 0px', marginRight: '20px', flexGrow: 1, marginLeft: '20px', maxWidth: '500px' }}>
          <SearchIcon style={{ color: '#1976d2', marginRight: '8px', width: '.7em', height: '.7em', marginLeft: '2px' }} />
          <InputBase
            placeholder="Search..."
            style={{ padding: '2px 0px 0px 0', width: '100%', border: 'none', outline: 'none', fontSize: '.8em' }}
            inputProps={{ 'aria-label': 'search' }}
          />
        </div>

        {/* Icon Group */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
          <IconButton aria-label="help" color="inherit" style={{ padding: '0px' }}>
            <HelpOutlineIcon />
          </IconButton>
          <IconButton aria-label="account of current user" color="inherit" style={{ padding: '0px' }}>
            <AccountCircleIcon />
          </IconButton>
          <IconButton aria-label="display more actions" color="inherit" style={{ padding: '0px' }}>
            <MoreVertIcon />
          </IconButton>
          {/* Time Display */}
          <div style={{ fontSize: '0.875rem', marginLeft: 'auto', paddingLeft: '8px', paddingRight: '16px', whiteSpace: 'nowrap' }}>
            {currentTime.toLocaleTimeString()}
          </div>
        </div>
      </Toolbar>
    </AppBar>
  );
};

export default Header;
