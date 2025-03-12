import { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AddPlayerForm from "./AddPlayerForm";

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [showForm, setShowForm] = useState(false);
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
          <button className="primary-button" onClick={() => setShowForm(!showForm)}>Add Player</button>
      </div>
      {showForm && <AddPlayerForm onPlayerAdded={fetchPlayers} />}
      <ul>{players.map((p) => <li key={p.id}>{p.name} - {p.team} ({p.position})</li>)}</ul>
    </div>
  );
};

export default Players;
