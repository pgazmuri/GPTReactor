import Typography from '@mui/material/Typography';

const Home = () => {
  return (
    <div style={{padding: 20}}>
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