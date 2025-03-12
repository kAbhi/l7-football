import { useState } from "react";
import axios from "axios";

const AddPlayerForm = ({ onPlayerAdded }: { onPlayerAdded: () => void }) => {
  const [name, setName] = useState("");
  const [team, setTeam] = useState("");
  const [position, setPosition] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    await axios.post("http://localhost:5000/players", { name, team, position });
    onPlayerAdded();
    setName("");
    setTeam("");
    setPosition("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Player Name" value={name} onChange={e => setName(e.target.value)} required />
      <input type="text" placeholder="Team" value={team} onChange={e => setTeam(e.target.value)} required />
      <input type="text" placeholder="Position" value={position} onChange={e => setPosition(e.target.value)} required />
      <button type="submit">Add Player</button>
    </form>
  );
};

export default AddPlayerForm;
