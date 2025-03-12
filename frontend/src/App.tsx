import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./components/Home";
import Matches from "./components/Matches";
import Teams from "./components/Teams";
import Players from "./components/Players";
import Areas from "./components/Areas";

const App = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/matches" element={<Matches />} />
      <Route path="/teams" element={<Teams />} />
      <Route path="/players" element={<Players />} />
      <Route path="/areas" element={<Areas />} />
    </Routes>
  </BrowserRouter>
);

export default App;
