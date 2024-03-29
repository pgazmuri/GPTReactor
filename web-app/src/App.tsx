import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ThemeProvider } from '@mui/material/styles';
import theme from './Theme';
import Sidebar from './components/Sidebar';
import Header from './components/Header';
import store from './store/store';
import Home from './pages/Home';

function App() {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <Router>
        <div style={{ display: 'flex', height: '100vh' }}>
          
          <div style={{ flexGrow: 1, display: 'flex', flexDirection: 'column' }}>
            <Header />
            <main style={{ background: '#f5f5f5', flexGrow: 1, overflowY: 'auto'}}>
            <div style={{ display: 'flex', height: 'calc(100vw - 64px)'  }}>
              <div style={{width: '150px'}}>
                <Sidebar />
              </div>
              <div style={{ width: 'calc(100vw - 150px)' }}>
                <Routes>
                  <Route path="/" element={<Home />} />
                  {/* Add additional routes as needed */}
                </Routes>
              </div>
            </div>
            </main>
          </div>
        </div>
        </Router>
      </ThemeProvider>
    </Provider>
  );
}

export default App;