import React from "react";
import { BrowserRouter, Route, Routes } from "react-router-dom";
import FaceSearch from "./pages/FaceSearch";

const App = () => {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<FaceSearch />} />
        {/* <Route path="*" element={<Error />} /> */}
      </Routes>
    </BrowserRouter>
  );
};

export default App;
