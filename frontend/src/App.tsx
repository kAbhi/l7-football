import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Matches from "./components/Matches";
import Teams from "./components/Teams";
import Players from "./components/Players";
import Areas from "./components/Areas";
import Admin from "./components/Admin";

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/matches" element={<Matches />} />
      <Route path="/teams" element={<Teams />} />
      <Route path="/players" element={<Players />} />
      <Route path="/areas" element={<Areas />} />
      <Route path="/admin" element={<Admin />} />
    </Routes>
  </BrowserRouter>
);

export default App;
