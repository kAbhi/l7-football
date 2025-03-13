import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";

const Players = () => {
  const [players, setPlayers] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchPlayers = async () => {
      try {
        const res = await axios.get("http://localhost:5000/players");
        setPlayers(res.data);
      } catch (error) {
        console.error("Error fetching players:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchPlayers();
  }, []);

  return (
    <div className="container">
      <h2>Players</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>

      {loading ? (
        <p>Loading players...</p>
      ) : players.length > 0 ? (
        <div className="cards">
          {players.map((player) => (
            <div key={player.id} className="card">
              <h3>{player.name}</h3>
              <p><strong>Team:</strong> {player.team}</p>
              <p><strong>Position:</strong> {player.position}</p>
            </div>
          ))}
        </div>
      ) : (
        <p>No players found.</p>
      )}
    </div>
  );
};

export default Players;
