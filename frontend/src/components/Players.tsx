import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Players = () => {
  const [players, setPlayers] = useState([]);
  const navigate = useNavigate();

  const fetchPlayers = async () => {
    const res = await axios.get("http://localhost:5000/players");
    setPlayers(res.data);
  };

  return (
    <div className="container">
      <h2>Players</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>
      <div className="button-group">
          <button className="primary-button" onClick={fetchPlayers}>Get Players</button>
      </div>
    </div>
  );
};

export default Players;
