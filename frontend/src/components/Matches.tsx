import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import AddMatchForm from "./AddMatchForm";

const Matches = () => {
  const [matches, setMatches] = useState([]);
  const navigate = useNavigate();

  // Fetch matches on page load
  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const res = await axios.get("http://localhost:5000/matches");
        setMatches(res.data);
      } catch (error) {
        console.error("Error fetching matches:", error);
      }
    };
    fetchMatches();
  }, []);

  return (
    <div className="container">
      <h2>Matches</h2>
      <button className="back-button" onClick={() => navigate("/")}>Back to Home</button>

      <div className="cards">
        {matches.map((match) => (
          <div key={match.id} className="card">
            <h3>{match.team1} vs {match.team2}</h3>
            <p><strong>Date:</strong> {match.date}</p>
            <p><strong>Location:</strong> {match.location}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Matches;
