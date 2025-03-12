import { useState } from "react";
import axios from "axios";

const AddMatchForm = ({ onMatchAdded }: { onMatchAdded: () => void }) => {
  const [team1, setTeam1] = useState("");
  const [team2, setTeam2] = useState("");
  const [date, setDate] = useState("");
  const [location, setLocation] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await axios.post("http://localhost:5000/matches", { team1, team2, date, location });
    onMatchAdded();
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Team 1" value={team1} onChange={e => setTeam1(e.target.value)} required />
      <input type="text" placeholder="Team 2" value={team2} onChange={e => setTeam2(e.target.value)} required />
      <input type="date" value={date} onChange={e => setDate(e.target.value)} required />
      <input type="text" placeholder="Location" value={location} onChange={e => setLocation(e.target.value)} required />
      <button type="submit">Add Match</button>
    </form>
  );
};

export default AddMatchForm;
