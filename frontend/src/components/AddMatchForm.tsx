import { useState } from "react";
import axios from "axios";

const AddMatchForm = ({ onMatchAdded }) => {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    try {
      await axios.post("http://localhost:5000/matches", { team1, team2, date, location });
      onMatchAdded(); // Refresh match list
      setTeam1("");
      setTeam2("");
      setDate("");
      setLocation("");
    } catch (err) {
      if (err.response && err.response.status === 400) {
        setError(err.response.data.error); // Display validation error
      } else {
        setError("Something went wrong. Please try again.");
      }
    }
  };

  return (
    <div>
      <h3>Add New Match</h3>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        <input type="text" value={team1} onChange={(e) => setTeam1(e.target.value)} placeholder="Team 1" required />
        <input type="text" value={team2} onChange={(e) => setTeam2(e.target.value)} placeholder="Team 2" required />
        <input type="date" value={date} onChange={(e) => setDate(e.target.value)} required />
        <input type="text" value={location} onChange={(e) => setLocation(e.target.value)} placeholder="Location" required />
        <button type="submit">Add Match</button>
      </form>
    </div>
  );
};

export default AddMatchForm;
