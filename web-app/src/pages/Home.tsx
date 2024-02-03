import Typography from '@mui/material/Typography';
import { useSelector } from 'react-redux';
import { RootState } from '../store/store'; // Corrected import path

const Home = () => {
  // Access the user's name from the Redux store
  const userName = useSelector((state: RootState) => state.user.name);

  return (
    <div style={{ padding: 20 }}>
      {/* Display a personalized greeting if the user's name is available */}
      {userName && <Typography variant="h5" gutterBottom>Hello, {userName}</Typography>}
      <Typography variant="h4" gutterBottom>
        Welcome to the Application Home Page
      </Typography>
      <Typography variant="body1">
        This is the body text. Use the navigation to switch between different sections of the application.
      </Typography>
      {/* You can add more components relevant to the Home page here */}
    </div>
  );
};

export default Home;