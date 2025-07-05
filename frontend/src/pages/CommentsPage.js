import React, { useState, useEffect, useContext } from 'react';
import { useParams } from 'react-router-dom';
import api from '../services/api';
import AuthContext from '../context/AuthContext';

const CommentsPage = () => {
  const { id } = useParams(); // Obtiene el ID del proveedor de la URL
  const [comments, setComments] = useState([]);
  const [newComment, setNewComment] = useState('');
  const { user } = useContext(AuthContext);

  const fetchComments = async () => {
    try {
      const response = await api.get(`/providers/${id}/comments/`);
      setComments(response.data);
    } catch (error) {
      console.error("Error fetching comments:", error);
    }
  };

  useEffect(() => {
    fetchComments();
  }, [id]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post(`/providers/${id}/comments/`, { body: newComment });
      setNewComment('');
      fetchComments(); // Refresca los comentarios
    } catch (error) {
      console.error("Error posting comment:", error);
    }
  };

  return (
    <div>
      <h2>Comentarios</h2>
      {user && (
        <form onSubmit={handleSubmit}>
          <textarea
            value={newComment}
            onChange={(e) => setNewComment(e.target.value)}
            placeholder="Escribe tu comentario..."
            required
          ></textarea>
          <button type="submit">Enviar Comentario</button>
        </form>
      )}
      <div className="comments-list">
        {comments.map(comment => (
          <div key={comment.id} className="comment-card">
            <p><strong>{comment.user.username}</strong> ({new Date(comment.created_at).toLocaleString()})</p>
            <p>{comment.body}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default CommentsPage;