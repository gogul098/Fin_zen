import axios from 'axios';

const api = axios.create({
    baseURL: 'http://localhost:8001',
    headers: {
        'Content-Type': 'application/json',
    },
});

export const getDashboardData = async (userId) => {
    try {
        const response = await api.get(`/dashboard/${userId}`);
        return response.data;
    } catch (error) {
        console.error("Error fetching dashboard data:", error);
        return null;
    }
};

export const sendChatMessage = async (userId, message) => {
    try {
        const response = await api.post('/chat', {
            user_id: userId,
            message: message
        });
        return response.data;
    } catch (error) {
        console.error("Error sending chat message:", error);
        return {
            role: "system",
            type: "text",
            content: "Sorry, I couldn't reach the server. Please try again."
        };
    }
};

export const updateContext = async (userId, text) => {
    try {
        const response = await api.post('/update-context', {
            user_id: userId,
            context_text: text
        });
        return response.data;
    } catch (error) {
        console.error("Error updating context:", error);
        return null;
    }
}

export default api;
