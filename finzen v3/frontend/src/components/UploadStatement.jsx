import React, { useState } from 'react';
import axios from 'axios';
import { Upload, CheckCircle, AlertCircle, FileText } from 'lucide-react';
import { motion } from 'framer-motion';

const UploadStatement = ({ userId = 1, onUploadComplete }) => {
    const [file, setFile] = useState(null);
    const [uploading, setUploading] = useState(false);
    const [status, setStatus] = useState(null); // 'success' | 'error' | null
    const [message, setMessage] = useState('');

    const handleFileChange = (e) => {
        if (e.target.files[0]) {
            setFile(e.target.files[0]);
            setStatus(null);
            setMessage('');
        }
    };

    const handleUpload = async () => {
        if (!file) return;

        setUploading(true);
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await axios.post(`http://localhost:8001/upload-pdf?user_id=${userId}`, formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                },
            });

            setStatus('success');
            setMessage(response.data.message);
            setFile(null);
            if (onUploadComplete) onUploadComplete();
        } catch (error) {
            console.error("Upload failed", error);
            setStatus('error');
            setMessage('Failed to upload. Please try again.');
        } finally {
            setUploading(false);
        }
    };

    return (
        <div className="bg-finzen-card p-6 rounded-xl border border-slate-700/50">
            <h3 className="text-lg font-bold mb-4 flex items-center gap-2">
                <FileText size={20} className="text-blue-400" />
                Upload Bank Statement
            </h3>

            <p className="text-sm text-finzen-muted mb-4">
                Upload your PDF bank statement to automatically track expenses.
                <br />
                <span className="text-xs text-yellow-500/80">
                    *File is securely analyzed and deleted immediately.
                </span>
            </p>

            <div className="space-y-4">
                <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-slate-600 border-dashed rounded-lg cursor-pointer bg-slate-800/50 hover:bg-slate-800 transition-colors">
                    <div className="flex flex-col items-center justify-center pt-5 pb-6">
                        <Upload className="w-8 h-8 mb-3 text-slate-400" />
                        <p className="text-sm text-slate-400">
                            {file ? file.name : "Click to upload or drag and drop"}
                        </p>
                        <p className="text-xs text-slate-500">PDF only (MAX. 5MB)</p>
                    </div>
                    <input type="file" className="hidden" accept=".pdf" onChange={handleFileChange} />
                </label>

                {file && (
                    <button
                        onClick={handleUpload}
                        disabled={uploading}
                        className="w-full py-2 px-4 bg-blue-600 hover:bg-blue-500 rounded-lg text-white font-medium transition-colors disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                    >
                        {uploading ? (
                            <>
                                <span className="w-4 h-4 border-2 border-white/20 border-t-white rounded-full animate-spin"></span>
                                Processing...
                            </>
                        ) : (
                            "Upload & Analyze"
                        )}
                    </button>
                )}

                {status === 'success' && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-3 bg-emerald-500/10 border border-emerald-500/30 rounded-lg text-emerald-400 text-sm flex items-center gap-2">
                        <CheckCircle size={16} />
                        {message}
                    </motion.div>
                )}

                {status === 'error' && (
                    <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="p-3 bg-red-500/10 border border-red-500/30 rounded-lg text-red-400 text-sm flex items-center gap-2">
                        <AlertCircle size={16} />
                        {message}
                    </motion.div>
                )}
            </div>
        </div>
    );
};

export default UploadStatement;
