import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import Dashboard from "./components/Dashboard";
import PackageList from "./components/PackageList";
import PackageDetails from "./components/PackageDetails";

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2", // You can customize these colors
    },
    secondary: {
      main: "#dc004e",
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <div className="App">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/packages" element={<PackageList />} />
            <Route path="/package/:id" element={<PackageDetails />} />
          </Routes>
        </div>
      </Router>
    </ThemeProvider>
  );
}

export default App;
