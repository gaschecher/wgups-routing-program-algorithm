import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Dashboard from "./components/Dashboard";
import PackageList from "./components/PackageList";
import PackageDetails from "./components/PackageDetails";

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/packages" element={<PackageList />} />
          <Route path="/package/:id" element={<PackageDetails />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
