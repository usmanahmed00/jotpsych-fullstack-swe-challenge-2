import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

const UserProfile = () => {
  const [profile, setProfile] = useState({ username: "", motto: "" });
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    const fetchProfile = async () => {
      try {
        const response = await fetch("http://localhost:3002/user", {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
        });
        if (!response.ok) {
          throw new Error("Error fetching user");
        }
        const data = await response.json();
        setProfile(data);
      } catch (error) {
        console.error("There was an error fetching the profile data!", error);
      }
    };

    fetchProfile();
  }, []);

  const handleLogout = async () => {
    try {
      const response = await fetch("http://localhost:3002/logout", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
      });
      if (!response.ok) {
        throw new Error("Error logging out");
      }
      localStorage.removeItem("token");
      setProfile({ username: "", motto: "" });
      navigate("/login");
    } catch (error) {
      console.error("There was an error logging out!", error);
    }
  };

  return (
    <div style={styles.container}>
      <div style={styles.profilePicture}></div>
      <div style={styles.username}>{profile.username}</div>
      <div style={styles.motto}>"{profile.motto}"</div>
      <button style={{ ...styles.button, ...styles.recordButton }}>
        Record (New) Motto
      </button>
      <button
        onClick={handleLogout}
        style={{ ...styles.button, ...styles.logoutButton }}
      >
        Logout
      </button>
    </div>
  );
};

const styles = {
  container: {
    textAlign: "center",
    margin: "50px",
    border: "1px solid #ccc",
    padding: "20px",
    borderRadius: "10px",
    width: "300px",
  },
  profilePicture: {
    width: "100px",
    height: "100px",
    borderRadius: "50%",
    backgroundColor: "#e0e0e0",
    margin: "0 auto",
    marginBottom: "20px",
  },
  username: {
    marginTop: "10px",
    fontSize: "20px",
    fontWeight: "bold",
  },
  motto: {
    fontSize: "24px",
    marginBottom: "20px",
  },
  button: {
    padding: "10px 20px",
    borderRadius: "5px",
    cursor: "pointer",
    marginRight: "10px",
    border: "none",
    fontSize: "16px",
  },
  recordButton: {
    backgroundColor: "#d4edda",
  },
  logoutButton: {
    backgroundColor: "#f8d7da",
  },
};
export default UserProfile;
