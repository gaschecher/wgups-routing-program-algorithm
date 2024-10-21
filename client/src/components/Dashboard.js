import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  TextField,
  Button,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Card,
  CardContent,
  CardHeader,
  Grid,
  Box,
} from "@mui/material";

const Dashboard = () => {
  const [packages, setPackages] = useState([]);
  const [mileage, setMileage] = useState(0);
  const [filters, setFilters] = useState({
    startTime: "",
    endTime: "",
    truckNumber: "",
    packageId: "",
  });

  useEffect(() => {
    fetchData();
  }, []);

  const formatTime = (timeStr) => {
    if (!timeStr) return "";
    // Remove any non-digit characters
    const digits = timeStr.replace(/\D/g, "");
    if (digits.length >= 4) {
      return `${digits.slice(0, 2)}:${digits.slice(2, 4)}`;
    }
    return timeStr;
  };

  const fetchData = async () => {
    try {
      const queryParams = new URLSearchParams();

      // Format and add time parameters
      const startTime = formatTime(filters.startTime);
      const endTime = formatTime(filters.endTime);

      if (startTime) queryParams.append("time", startTime);
      if (endTime) queryParams.append("end_time", endTime);
      if (filters.truckNumber) queryParams.append("truck", filters.truckNumber);
      if (filters.packageId)
        queryParams.append("package_id", filters.packageId);

      let url = "/api/packages";
      if (filters.packageId) {
        url = `/api/package/${filters.packageId}`;
      }

      const response = await fetch(`${url}?${queryParams}`);
      if (!response.ok) {
        throw new Error("Failed to fetch data");
      }

      let data = await response.json();

      // If single package response, convert to array
      if (!Array.isArray(data)) {
        data = [data];
      }

      // Format the data to match the display requirements
      const formattedPackages = data.map((pkg) => ({
        ...pkg,
        delivery_time: pkg.delivery_time
          ? new Date(pkg.delivery_time).toLocaleTimeString("en-US", {
              hour: "2-digit",
              minute: "2-digit",
              second: "2-digit",
              hour12: false,
            })
          : "N/A",
        deadline: pkg.deadline || "EOD",
        truck: pkg.truck || "Not Assigned",
      }));

      setPackages(formattedPackages);

      // Fetch mileage
      const mileageResponse = await fetch(`/api/mileage?${queryParams}`);
      if (!mileageResponse.ok) {
        throw new Error("Failed to fetch mileage");
      }
      const mileageData = await mileageResponse.json();
      setMileage(mileageData.total_mileage);
    } catch (error) {
      console.error("Error fetching data:", error);
      setPackages([]);
      setMileage(0);
    }
  };

  const handleFilterChange = (field) => (event) => {
    const value = event.target.value;

    // Handle time formatting
    if (field === "startTime" || field === "endTime") {
      const formattedTime = formatTime(value);
      setFilters((prev) => ({
        ...prev,
        [field]: formattedTime,
      }));
    } else {
      setFilters((prev) => ({
        ...prev,
        [field]: value,
      }));
    }
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    fetchData();
  };

  const handleReset = () => {
    setFilters({
      startTime: "",
      endTime: "",
      truckNumber: "",
      packageId: "",
    });
    setTimeout(fetchData, 0);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h3" component="h1" gutterBottom align="center">
        Package Delivery Dashboard
      </Typography>

      <Paper
        component="form"
        onSubmit={handleSubmit}
        elevation={3}
        sx={{ p: 3, mb: 3 }}
      >
        <Grid container spacing={2} alignItems="center">
          <Grid item xs={12} md={2.5}>
            <TextField
              fullWidth
              label="Start Time"
              placeholder="HH:MM"
              value={filters.startTime}
              onChange={handleFilterChange("startTime")}
              helperText="24-hour format (HH:MM)"
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
          <Grid item xs={12} md={2.5}>
            <TextField
              fullWidth
              label="End Time"
              placeholder="HH:MM"
              value={filters.endTime}
              onChange={handleFilterChange("endTime")}
              helperText="24-hour format (HH:MM)"
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
          <Grid item xs={12} md={2.5}>
            <TextField
              fullWidth
              label="Truck Number"
              type="number"
              value={filters.truckNumber}
              onChange={handleFilterChange("truckNumber")}
              inputProps={{ min: 1, max: 3 }}
              helperText="Enter 1, 2, or 3"
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
          <Grid item xs={12} md={2.5}>
            <TextField
              fullWidth
              label="Package ID"
              type="number"
              value={filters.packageId}
              onChange={handleFilterChange("packageId")}
              inputProps={{ min: 1, max: 40 }}
              helperText="Enter package number"
              InputLabelProps={{
                shrink: true,
              }}
            />
          </Grid>
          <Grid item xs={12} md={2}>
            <Box sx={{ display: "flex", gap: 1 }}>
              <Button
                variant="contained"
                type="submit"
                sx={{ flex: 1, height: "56px" }}
              >
                SEARCH
              </Button>
              <Button
                variant="outlined"
                onClick={handleReset}
                sx={{ flex: 1, height: "56px" }}
              >
                RESET
              </Button>
            </Box>
          </Grid>
        </Grid>
      </Paper>

      <Card sx={{ mb: 3 }}>
        <CardHeader title="Total Mileage" />
        <CardContent>
          <Typography variant="h4" component="p">
            {mileage.toFixed(1)} miles
          </Typography>
        </CardContent>
      </Card>

      <TableContainer component={Paper}>
        <Table sx={{ minWidth: 650 }} aria-label="package table">
          <TableHead>
            <TableRow>
              <TableCell>ID</TableCell>
              <TableCell>Address</TableCell>
              <TableCell>Deadline</TableCell>
              <TableCell>Weight</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Delivery Time</TableCell>
              <TableCell>Truck</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {packages.map((pkg) => (
              <TableRow key={pkg.id}>
                <TableCell>{pkg.id}</TableCell>
                <TableCell>{`${pkg.address}, ${pkg.city}, ${pkg.state} ${pkg.zip}`}</TableCell>
                <TableCell>{pkg.deadline}</TableCell>
                <TableCell>{pkg.weight} kg</TableCell>
                <TableCell>{pkg.status}</TableCell>
                <TableCell>{pkg.delivery_time}</TableCell>
                <TableCell>{pkg.truck}</TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Container>
  );
};

export default Dashboard;
