const ResumeCard = ({ resume, rank, onClick, onInterview }) => {
    const score = resume.score || (resume.similarity_score ? resume.similarity_score * 10 : 0);
    const isHighMatch = score >= 8;

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: rank * 0.1 }}
            className="relative group bg-white/5 hover:bg-white/10 border border-white/5 hover:border-tropical-400/50 rounded-3xl p-6 cursor-pointer transition-all hover:scale-[1.02] hover:shadow-[0_10px_30px_rgba(0,0,0,0.2)] mb-4 flex items-center justify-between overflow-hidden"
            onClick={() => onClick(resume)}
        >
            <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/5 to-transparent translate-x-[-200%] group-hover:translate-x-[200%] transition-transform duration-1000"></div>

            <div className="flex items-center gap-6 relative z-10">
                <div className={`w-16 h-16 rounded-2xl flex items-center justify-center font-black text-2xl ${isHighMatch ? 'bg-tropical-400 text-forest-900 shadow-[0_0_20px_rgba(46,230,200,0.4)]' : 'bg-white/10 text-white/50'}`}>
                    {typeof score === 'number' ? score.toFixed(1) : score}
                </div>
                <div>
                    <h3 className="text-xl font-bold text-white mb-1 group-hover:text-tropical-300 transition-colors">{resume.name || 'Candidate'}</h3>
                    <div className="flex flex-wrap gap-2 text-xs font-bold text-white/40 uppercase tracking-widest">
                        <span>{resume.email}</span>
                        <span className="text-tropical-400">•</span>
                        <span>{resume.experience_years || 0} Years Exp</span>
                        {resume.jd_domain && (
                            <>
                                <span className="text-tropical-400">•</span>
                                <span className="text-gold-300">{resume.jd_domain}</span>
                            </>
                        )}
                    </div>
                </div>
            </div>

            <div className="flex items-center gap-4 relative z-10">
                {/* Interview Action */}
                <button
                    onClick={(e) => { e.stopPropagation(); onInterview(resume); }}
                    className="w-12 h-12 rounded-full bg-forest-900 border border-tropical-400/30 text-tropical-400 flex items-center justify-center hover:bg-tropical-400 hover:text-forest-900 transition-all shadow-lg hover:shadow-[0_0_20px_rgba(46,230,200,0.4)] group-hover:scale-110"
                    title="Start AI Interview"
                >
                    <i className="fas fa-microphone-alt"></i>
                </button>

                <div className="w-10 h-10 rounded-full border border-white/10 flex items-center justify-center group-hover:border-tropical-400/50 transition-colors">
                    <i className="fas fa-chevron-right text-white/20 group-hover:text-tropical-400 transition-colors"></i>
                </div>
            </div>
        </motion.div>
    );
};
