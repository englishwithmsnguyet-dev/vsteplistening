/* ==========================================================================
   VSTEP LISTENING - WEB APPLICATION CONTROLLER (app.js)
   ========================================================================== */

class VstepApp {
    constructor() {
        this.data = null;
        this.studentName = sessionStorage.getItem('vstep_student_name') || ""; // Session-based student name (resets when closing tab/browser)
        this.allowedClasses = ['ONB103', 'CB206', 'CB210', 'CB211', 'CB213', 'B212'];
        this.progress = {
            completedTests: {}, // testId -> score
            completedTheory: {}, // theoryId -> true
            history: [] // list of completed sessions
        };
        
        // Active Practice State
        this.activeSession = {
            part: null,
            id: null,
            isTheory: false,
            data: null, // the active practice/theory object
            userAnswers: {}, // qNumber -> selectedLetter
            submitted: false
        };
        
        // DOM Elements cache
        this.elements = {};
        
        // Audio state
        this.audioPlaying = false;
        this.audioDuration = 0;
        
        // Initialize App on DOM load
        window.addEventListener('DOMContentLoaded', () => this.init());
    }

    async init() {
        // Clear any legacy permanent unlock state from localStorage
        localStorage.removeItem('vstep_unlocked');

        this.cacheElements();
        this.setupEventListeners();
        this.loadTheme();
        this.loadProgress();
        this.checkStudentName();
        
        try {
            await this.loadData();
            this.renderLists();
            this.renderVocab();
            this.applyLocks();
            this.updateStats();
        } catch (err) {
            console.error("Failed to load project database:", err);
            alert("Không thể tải cơ sở dữ liệu học tập. Vui lòng chạy máy chủ cục bộ hoặc thử lại!");
        }
        
        // Route initial hash or default to dashboard
        this.handleRouting();
        window.addEventListener('hashchange', () => this.handleRouting());
    }

    cacheElements() {
        // Navigation & Layout
        this.elements.sidebar = document.getElementById('app-sidebar');
        this.elements.mobileToggle = document.getElementById('mobile-toggle-btn');
        this.elements.mobileClose = document.getElementById('mobile-close-btn');
        this.elements.themeToggle = document.getElementById('theme-toggle');
        this.elements.overallProgressFill = document.getElementById('overall-progress-bar');
        this.elements.overallProgressText = document.getElementById('overall-progress-text');
        this.elements.currentBc = document.getElementById('current-bc');
        this.elements.parentBc = document.getElementById('parent-bc');
        
        // Dashboard Stats
        this.elements.statsTheory = document.getElementById('stats-theory-done');
        this.elements.statsTests = document.getElementById('stats-tests-done');
        this.elements.statsAccuracy = document.getElementById('stats-accuracy');
        this.elements.statsTableBody = document.getElementById('stats-table-body');
        this.elements.clearStatsBtn = document.getElementById('clear-stats-btn');
        
        // Part lists containers
        this.elements.p1TheoryList = document.getElementById('p1-theory-list');
        this.elements.p1PracticeList = document.getElementById('p1-practice-list');
        this.elements.p2PracticeList = document.getElementById('p2-practice-list');
        this.elements.p3PracticeList = document.getElementById('p3-practice-list');
        
        // Custom Audio Player
        this.elements.audio = document.getElementById('native-audio');
        this.elements.playBtn = document.getElementById('audio-play-btn');
        this.elements.progressSlider = document.getElementById('audio-progress-slider');
        this.elements.progressFill = document.getElementById('audio-progress-fill');
        this.elements.progressHandle = document.getElementById('audio-progress-handle');
        this.elements.currentTimeText = document.getElementById('audio-current-time');
        this.elements.totalTimeText = document.getElementById('audio-total-time');
        this.elements.speedBtn = document.getElementById('audio-speed-btn');
        this.elements.speedDropdown = document.getElementById('audio-speed-dropdown');
        this.elements.playerTitle = document.getElementById('player-title');
        this.elements.playerPartBadge = document.getElementById('player-part-badge');
        
        // Quiz & Explanation
        this.elements.mainPlayerCard = document.getElementById('main-player-card');
        this.elements.questionsList = document.getElementById('practice-questions-list');
        this.elements.submitBtn = document.getElementById('submit-practice-btn');

        // Student Name Elements
        this.elements.welcomeModal = document.getElementById('welcome-modal');
        this.elements.studentNameInput = document.getElementById('student-name-input');
        this.elements.studentClassInput = document.getElementById('student-class-input');
        this.elements.sidebarUserName = document.getElementById('sidebar-user-name');
        this.elements.userAvatarChar = document.getElementById('user-avatar-char');
        this.elements.editNameBtn = document.getElementById('edit-name-btn');
        this.elements.exportCumulativeReportBtn = document.getElementById('export-cumulative-report-btn');
        
        // Practice Report Card
        this.elements.practiceReportCard = document.getElementById('practice-report-card');
        this.elements.reportStudentName = document.getElementById('report-student-name');
        this.elements.reportTestTitle = document.getElementById('report-test-title');
        this.elements.reportScore = document.getElementById('report-score');
        this.elements.reportAccuracy = document.getElementById('report-accuracy');
    }

    setupEventListeners() {
        // Mobile Sidebar Toggles
        this.elements.mobileToggle.addEventListener('click', () => {
            this.elements.sidebar.classList.add('mobile-open');
        });
        
        this.elements.mobileClose.addEventListener('click', () => {
            this.elements.sidebar.classList.remove('mobile-open');
        });
        
        // Sidebar Links
        document.querySelectorAll('.menu-item').forEach(item => {
            item.addEventListener('click', (e) => {
                this.elements.sidebar.classList.remove('mobile-open');
            });
        });
        
        // Theme Toggle
        this.elements.themeToggle.addEventListener('click', () => this.toggleTheme());
        
        // Part 1 Tabs
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const tabId = btn.getAttribute('data-tab');
                const container = btn.closest('.tab-container');
                
                // Toggle active buttons
                container.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Toggle active panes
                container.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                container.querySelector(`#tab-${tabId}`).classList.add('active');
                
                // Reset search when switching vocabulary tabs
                if (tabId.startsWith('vocab-cat-')) {
                    const searchInput = document.getElementById('vocab-search');
                    if (searchInput) {
                        searchInput.value = '';
                        document.querySelectorAll('.vocab-topic-block, .vocab-card').forEach(el => {
                            el.style.display = '';
                        });
                    }
                }
            });
        });
        
        // Custom Audio Player Events
        this.elements.playBtn.addEventListener('click', () => this.toggleAudio());
        
        // Audio metadata loaded
        this.elements.audio.addEventListener('loadedmetadata', () => {
            this.audioDuration = this.elements.audio.duration;
            this.elements.totalTimeText.textContent = this.formatTime(this.audioDuration);
        });
        
        // Audio progress update
        this.elements.audio.addEventListener('timeupdate', () => {
            if (!this.elements.audio.seeking) {
                const curTime = this.elements.audio.currentTime;
                this.elements.currentTimeText.textContent = this.formatTime(curTime);
                const percent = (curTime / this.audioDuration) * 100;
                this.elements.progressFill.style.width = `${percent}%`;
                this.elements.progressHandle.style.left = `${percent}%`;
            }
        });
        
        // Audio ended
        this.elements.audio.addEventListener('ended', () => {
            this.setAudioState(false);
            this.elements.audio.currentTime = 0;
            this.elements.progressFill.style.width = '0%';
            this.elements.progressHandle.style.left = '0%';
            this.elements.currentTimeText.textContent = '0:00';
        });
        
        // Progress bar slider interaction
        const handleSliderClick = (e) => {
            const rect = this.elements.progressSlider.getBoundingClientRect();
            const clickX = e.clientX - rect.left;
            const percent = Math.max(0, Math.min(100, (clickX / rect.width) * 100));
            this.elements.progressFill.style.width = `${percent}%`;
            this.elements.progressHandle.style.left = `${percent}%`;
            this.elements.audio.currentTime = (percent / 100) * this.audioDuration;
        };
        
        this.elements.progressSlider.addEventListener('mousedown', (e) => {
            handleSliderClick(e);
            
            const onMouseMove = (moveEvent) => {
                handleSliderClick(moveEvent);
            };
            
            const onMouseUp = () => {
                document.removeEventListener('mousemove', onMouseMove);
                document.removeEventListener('mouseup', onMouseUp);
            };
            
            document.addEventListener('mousemove', onMouseMove);
            document.addEventListener('mouseup', onMouseUp);
        });
        
        // Speed Toggle Dropdown
        this.elements.speedBtn.addEventListener('click', (e) => {
            e.stopPropagation();
            this.elements.speedDropdown.classList.toggle('hidden');
        });
        
        document.querySelectorAll('.speed-option').forEach(opt => {
            opt.addEventListener('click', (e) => {
                const speed = parseFloat(opt.getAttribute('data-speed'));
                this.elements.audio.playbackRate = speed;
                this.elements.speedBtn.textContent = `${speed.toFixed(2)}x`;
                
                document.querySelectorAll('.speed-option').forEach(o => o.classList.remove('active'));
                opt.classList.add('active');
                this.elements.speedDropdown.classList.add('hidden');
            });
        });
        
        document.addEventListener('click', () => {
            this.elements.speedDropdown.classList.add('hidden');
        });

        // Quiz Submission (Global)
        this.elements.submitBtn.addEventListener('click', () => this.submitPractice());
        
        // Single Quiz Submission (Theory)
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('btn-submit-single')) {
                const qNum = e.target.getAttribute('data-q-num');
                this.submitSingleTheoryItem(qNum);
            }
        });
        document.addEventListener('click', (e) => {
            if (e.target.classList.contains('inline-tab-btn')) {
                const btn = e.target;
                const paneId = btn.getAttribute('data-inline-tab');
                const inlinePanel = btn.closest('.practice-explanation-panel');
                
                inlinePanel.querySelectorAll('.inline-tab-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                inlinePanel.querySelectorAll('.drawer-pane').forEach(p => p.classList.remove('active'));
                const targetPane = inlinePanel.querySelector(`.drawer-pane[data-pane="${paneId}"]`);
                if (targetPane) targetPane.classList.add('active');
            }
        });
        
        // Clear Statistics
        this.elements.clearStatsBtn.addEventListener('click', () => this.clearProgress());

        // Student Name Event Listeners
        this.elements.editNameBtn.addEventListener('click', () => this.editStudentName());
        this.elements.exportCumulativeReportBtn.addEventListener('click', () => this.exportCumulativeReport());
    }

    /* --- DATA LOADING & RENDERING --- */
    async loadData() {
        if (window.VSTEP_DATA) {
            this.data = window.VSTEP_DATA;
        } else {
            const res = await fetch('data.json');
            this.data = await res.json();
        }
    }

    renderLists() {
        // Part 1 Theory List
        this.elements.p1TheoryList.innerHTML = this.data.part1.theory.map(t => {
            const isCompleted = this.progress.completedTheory[t.id];
            const isLocked = !this.isItemUnlocked(1, t.id, true);
            
            return `
                <div class="list-item-card ${isCompleted ? 'completed' : ''} ${isLocked ? 'locked' : ''}" 
                     ${isLocked ? `onclick="app.promptUnlock(1, '${t.id}', true, () => app.startPractice(1, '${t.id}', true))"` : `onclick="app.startPractice(1, '${t.id}', true)"`}>
                    <div class="card-title-row">
                        <h4>${t.title}</h4>
                        ${isCompleted ? '<span class="completed-badge">Đã học</span>' : ''}
                        ${isLocked ? '<span class="locked-badge">Khóa</span>' : ''}
                    </div>
                    <p class="card-description">Tìm hiểu các điểm ngữ pháp, cấu trúc từ vựng và luyện tập nghe 4 ví dụ cụ thể của dạng bài này.</p>
                    <div class="card-footer-stats">
                        <span>Luyện nghe: <strong>4 Ví dụ</strong></span>
                        <span>Độ khó: <strong>B1-B2</strong></span>
                    </div>
                </div>
            `;
        }).join('');

        // Part 1 Practice List
        this.elements.p1PracticeList.innerHTML = this.data.part1.practice.map(p => {
            const score = this.progress.completedTests[p.id];
            const isCompleted = score !== undefined;
            const isLocked = !this.isItemUnlocked(1, p.id, false);
            return `
                <div class="list-item-card ${isCompleted ? 'completed' : ''} ${isLocked ? 'locked' : ''}" 
                     ${isLocked ? `onclick="app.promptUnlock(1, '${p.id}', false, () => app.startPractice(1, '${p.id}', false))"` : `onclick="app.startPractice(1, '${p.id}', false)"`}>
                    <div class="card-title-row">
                        <h4>${p.title}</h4>
                        ${isCompleted ? `<span class="completed-badge">${score}/8 Câu</span>` : ''}
                        ${isLocked ? '<span class="locked-badge">Khóa</span>' : ''}
                    </div>
                    <p class="card-description">Đề luyện tập tổng hợp bao gồm 8 thông báo ngắn đơn lẻ. Có lời thoại dịch nghĩa chi tiết.</p>
                    <div class="card-footer-stats">
                        <span>Đề thi: <strong>8 Câu hỏi</strong></span>
                        <span>Thời lượng: <strong>~ 5 phút</strong></span>
                    </div>
                </div>
            `;
        }).join('');

        // Part 2 Practice List
        this.elements.p2PracticeList.innerHTML = this.data.part2.practice.map(p => {
            const score = this.progress.completedTests[p.id];
            const isCompleted = score !== undefined;
            const isLocked = !this.isItemUnlocked(2, p.id, false);
            return `
                <div class="list-item-card ${isCompleted ? 'completed' : ''} ${isLocked ? 'locked' : ''}" 
                     ${isLocked ? `onclick="app.promptUnlock(() => app.startPractice(2, '${p.id}', false))"` : `onclick="app.startPractice(2, '${p.id}', false)"`}>
                    <div class="card-title-row">
                        <h4>${p.title}</h4>
                        ${isCompleted ? `<span class="completed-badge">${score}/4 Câu</span>` : ''}
                        ${isLocked ? '<span class="locked-badge">Khóa</span>' : ''}
                    </div>
                    <p class="card-description">Luyện nghe hội thoại dài giữa 2 người nói. Rèn luyện kỹ năng định vị thông tin trong đoạn đối thoại lớn.</p>
                    <div class="card-footer-stats">
                        <span>Hội thoại: <strong>4 Câu hỏi</strong></span>
                        <span>Độ khó: <strong>B2-C1</strong></span>
                    </div>
                </div>
            `;
        }).join('');

        // Part 3 Practice List
        this.elements.p3PracticeList.innerHTML = this.data.part3.practice.map(p => {
            const score = this.progress.completedTests[p.id];
            const isCompleted = score !== undefined;
            const isLocked = !this.isItemUnlocked(3, p.id, false);
            return `
                <div class="list-item-card ${isCompleted ? 'completed' : ''} ${isLocked ? 'locked' : ''}" 
                     ${isLocked ? `onclick="app.promptUnlock(() => app.startPractice(3, '${p.id}', false))"` : `onclick="app.startPractice(3, '${p.id}', false)"`}>
                    <div class="card-title-row">
                        <h4>${p.title}</h4>
                        ${isCompleted ? `<span class="completed-badge">${score}/5 Câu</span>` : ''}
                        ${isLocked ? '<span class="locked-badge">Khóa</span>' : ''}
                    </div>
                    <p class="card-description">Luyện nghe bài phát biểu hoặc bài giảng học thuật của một học giả. Đòi hỏi khả năng nghe hiểu chuyên sâu.</p>
                    <div class="card-footer-stats">
                        <span>Bài giảng: <strong>5 Câu hỏi</strong></span>
                        <span>Độ khó: <strong>B2-C1</strong></span>
                    </div>
                </div>
            `;
        }).join('');
    }

    /* --- APPLICATION ROUTING --- */
    handleRouting() {
        const hash = window.location.hash.replace('#', '') || 'dashboard';
        const validViews = ['dashboard', 'part1', 'part1-vocab', 'part2', 'part3', 'statistics', 'practice-run'];
        
        if ((hash === 'part2' || hash === 'part3') && !this.isItemUnlocked(hash === 'part2' ? 2 : 3, '', false)) {
            this.promptUnlock(hash === 'part2' ? 2 : 3, '', false, () => {
                window.location.hash = '#' + hash;
            });
            window.location.hash = '#dashboard';
            return;
        }
        
        if (validViews.includes(hash)) {
            // If exiting practice, make sure audio is stopped
            if (hash !== 'practice-run' && this.elements.audio.src) {
                this.stopAudio();
            }
            this.switchView(hash);
        } else {
            this.switchView('dashboard');
        }
    }

    getAllowedPasswords(partNum, id, isTheory = false) {
        if (partNum === 1) {
            if (isTheory) {
                if (id === 'p1_type_01' || id === 'p1_type_02') {
                    return ['ONB103', 'CB206', 'CB210', 'CB211', 'CB213', 'B212', 'missnguyet2026'];
                }
                if (id === 'p1_type_03') {
                    return ['ONB103', 'CB206', 'CB210', 'CB211', 'CB213', 'missnguyet2026'];
                }
                if (id === 'p1_type_04') {
                    return ['CB206', 'CB210', 'CB211', 'CB213'];
                }
                if (id === 'p1_type_05' || id === 'p1_type_06') {
                    return ['CB206', 'CB210', 'CB211'];
                }
            } else {
                // Đề Practice Part 1
                return ['CB206', 'CB210', 'CB211'];
            }
        } else if (partNum === 2) {
            // Part 2
            return ['CB206', 'CB210'];
        } else if (partNum === 3) {
            // Part 3
            return ['CB206'];
        }
        return ['ONB103', 'CB206', 'CB210', 'CB211', 'CB213', 'B212', 'missnguyet2026'];
    }

    getUnlockedItems() {
        try {
            return JSON.parse(sessionStorage.getItem('vstep_unlocked_items') || '[]');
        } catch (e) {
            return [];
        }
    }

    addUnlockedItem(id) {
        const items = this.getUnlockedItems();
        if (!items.includes(id)) {
            items.push(id);
            sessionStorage.setItem('vstep_unlocked_items', JSON.stringify(items));
        }
    }

    isItemUnlocked(partNum, id, isTheory = false) {
        if (sessionStorage.getItem('vstep_unlocked') === 'true') {
            return true;
        }
        
        const lockKey = isTheory ? `theory_${partNum}_${id}` : `practice_${partNum}_${id}`;
        const items = this.getUnlockedItems();
        return items.includes(lockKey);
    }

    promptUnlock(partNum, id, isTheory, successCallback) {
        const allowed = this.getAllowedPasswords(partNum, id, isTheory).map(p => p.toUpperCase());
        const pwd = prompt("Vui lòng nhập mật khẩu mở khóa phần này:");
        if (pwd) {
            const cleanPwd = pwd.trim().toUpperCase();
            if (allowed.includes(cleanPwd)) {
                if (cleanPwd === 'MISSNGUYET2026') {
                    sessionStorage.setItem('vstep_unlocked', 'true');
                } else {
                    const lockKey = isTheory ? `theory_${partNum}_${id}` : `practice_${partNum}_${id}`;
                    this.addUnlockedItem(lockKey);
                }
                
                alert("Mở khóa thành công!");
                this.applyLocks();
                this.renderLists();
                if (typeof successCallback === 'function') {
                    successCallback();
                }
                return;
            }
        }
        if (pwd !== null) {
            alert("Mật khẩu không chính xác hoặc lớp của bạn chưa được cấp quyền truy cập mục này!");
        }
    }

    applyLocks() {
        const unlockedP2 = this.isItemUnlocked(2, '', false);
        const unlockedP3 = this.isItemUnlocked(3, '', false);
        
        // Update Sidebar menu items
        const p2MenuItem = document.querySelector('.menu-item[data-view="part2"]');
        const p3MenuItem = document.querySelector('.menu-item[data-view="part3"]');
        
        if (!unlockedP2) {
            if (p2MenuItem) {
                p2MenuItem.classList.add('locked');
                p2MenuItem.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.promptUnlock(2, '', false, () => {
                        this.switchView('part2');
                        const menuBtn = document.querySelector('.menu-item[data-view="part2"]');
                        if (menuBtn) {
                            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
                            menuBtn.classList.add('active');
                        }
                    });
                };
            }
        } else {
            if (p2MenuItem) {
                p2MenuItem.classList.remove('locked');
                p2MenuItem.onclick = null;
            }
        }
        
        if (!unlockedP3) {
            if (p3MenuItem) {
                p3MenuItem.classList.add('locked');
                p3MenuItem.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.promptUnlock(3, '', false, () => {
                        this.switchView('part3');
                        const menuBtn = document.querySelector('.menu-item[data-view="part3"]');
                        if (menuBtn) {
                            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
                            menuBtn.classList.add('active');
                        }
                    });
                };
            }
        } else {
            if (p3MenuItem) {
                p3MenuItem.classList.remove('locked');
                p3MenuItem.onclick = null;
            }
        }
        
        // Update Dashboard cards
        const p2Card = document.querySelector('.part-card[data-view="part2"]');
        const p3Card = document.querySelector('.part-card[data-view="part3"]');
        
        if (!unlockedP2) {
            if (p2Card) {
                p2Card.classList.add('locked');
                p2Card.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.promptUnlock(2, '', false, () => {
                        this.switchView('part2');
                        const menuBtn = document.querySelector('.menu-item[data-view="part2"]');
                        if (menuBtn) {
                            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
                            menuBtn.classList.add('active');
                        }
                    });
                };
                const btn = p2Card.querySelector('.card-action-btn');
                if (btn) {
                    btn.innerHTML = `
                        <span>Đang khóa</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    `;
                }
            }
        } else {
            if (p2Card) {
                p2Card.classList.remove('locked');
                p2Card.onclick = null;
                const btn = p2Card.querySelector('.card-action-btn');
                if (btn) {
                    btn.innerHTML = `
                        <span>Bắt đầu ôn tập</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    `;
                }
            }
        }
        
        if (!unlockedP3) {
            if (p3Card) {
                p3Card.classList.add('locked');
                p3Card.onclick = (e) => {
                    e.preventDefault();
                    e.stopPropagation();
                    this.promptUnlock(3, '', false, () => {
                        this.switchView('part3');
                        const menuBtn = document.querySelector('.menu-item[data-view="part3"]');
                        if (menuBtn) {
                            document.querySelectorAll('.menu-item').forEach(m => m.classList.remove('active'));
                            menuBtn.classList.add('active');
                        }
                    });
                };
                const btn = p3Card.querySelector('.card-action-btn');
                if (btn) {
                    btn.innerHTML = `
                        <span>Đang khóa</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0 1 10 0v4"/></svg>
                    `;
                }
            }
        } else {
            if (p3Card) {
                p3Card.classList.remove('locked');
                p3Card.onclick = null;
                const btn = p3Card.querySelector('.card-action-btn');
                if (btn) {
                    btn.innerHTML = `
                        <span>Bắt đầu ôn tập</span>
                        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
                    `;
                }
            }
        }
    }

    switchView(viewName) {
        if ((viewName === 'part2' || viewName === 'part3') && !this.isItemUnlocked(viewName === 'part2' ? 2 : 3, '', false)) {
            this.promptUnlock(viewName === 'part2' ? 2 : 3, '', false, () => {
                this.switchView(viewName);
            });
            return;
        }

        // Toggle topbar brand position
        const topbar = document.querySelector('.topbar');
        if (topbar) {
            if (viewName === 'dashboard') {
                topbar.classList.remove('view-active');
            } else {
                topbar.classList.add('view-active');
            }
        }

        // Toggle view panels
        document.querySelectorAll('.view-panel').forEach(panel => {
            panel.classList.remove('active');
        });
        const activePanel = document.getElementById(`view-${viewName}`);
        if (activePanel) {
            activePanel.classList.add('active');
        }
        
        // Update Sidebar menu
        document.querySelectorAll('.menu-item').forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('data-view') === viewName) {
                item.classList.add('active');
            }
        });
        
        // Map Sidebar section labels for Part 1/2/3 to breadcrumbs
        const viewTitles = {
            'dashboard': { parent: 'Học nghe VSTEP', current: 'HOME PAGE' },
            'part1': { parent: 'Luyện tập', current: 'PART 01: SHORT TALKS/CONVERSATIONS' },
            'part1-vocab': { parent: 'Từ vựng', current: 'Từ vựng PART 01' },
            'part2': { parent: 'Luyện tập', current: 'PART 02: LONG CONVERSATIONS' },
            'part3': { parent: 'Luyện tập', current: 'PART 03: LONG TALKS' },
            'statistics': { parent: 'Tiện ích', current: 'Tiến độ học tập' },
            'practice-run': { parent: 'Phòng thi', current: 'Đang làm bài nghe' }
        };
        
        const titles = viewTitles[viewName] || { parent: 'Học nghe VSTEP', current: 'Học tập' };
        this.elements.parentBc.textContent = titles.parent;
        this.elements.currentBc.textContent = titles.current;
        
        // Scroll to top of panel
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }

    renderVocab() {
        if (!window.VSTEP_VOCAB_DATA) return;
        
        window.VSTEP_VOCAB_DATA.forEach((cat, cIdx) => {
            const container = document.getElementById(`tab-vocab-cat-${cIdx}`);
            if (!container) return;
            
            let html = '';
            cat.topics.forEach(topic => {
                let emoji = "📝";
                const nameUpper = topic.name.toUpperCase();
                if (nameUpper.includes("GIÁO DỤC")) emoji = "🏫";
                else if (nameUpper.includes("KHOA HỌC")) emoji = "🧪";
                else if (nameUpper.includes("Y TẾ") || nameUpper.includes("MEDICAL")) emoji = "🏥";
                else if (nameUpper.includes("KINH DOANH") || nameUpper.includes("OFFICE")) emoji = "🏢";
                else if (nameUpper.includes("XÂY DỰNG") || nameUpper.includes("WAREHOUSE")) emoji = "🏗️";
                else if (nameUpper.includes("NGHỆ THUẬT") || nameUpper.includes("THEATER")) emoji = "🎭";
                else if (nameUpper.includes("LUẬT")) emoji = "⚖️";
                else if (nameUpper.includes("THỦ CÔNG")) emoji = "🛠️";
                else if (nameUpper.includes("LOGISTICS") || nameUpper.includes("KHO VẬN")) emoji = "📦";
                else if (nameUpper.includes("RESTAURANT") || nameUpper.includes("SHOP")) emoji = "🛍️";
                else if (nameUpper.includes("HOTEL")) emoji = "🏨";
                else if (nameUpper.includes("BANK")) emoji = "🏦";
                else if (nameUpper.includes("POST OFFICE")) emoji = "📮";
                else if (nameUpper.includes("AIRPORT")) emoji = "✈️";
                else if (nameUpper.includes("REAL ESTATE")) emoji = "🏠";
                else if (nameUpper.includes("TRAIN") || nameUpper.includes("STATION")) emoji = "🚆";
                else if (nameUpper.includes("SỰ KIỆN")) emoji = "🎉";
                
                html += `
                    <div class="vocab-topic-block">
                        <h3 class="vocab-topic-title">${emoji} ${topic.name}</h3>
                        <div class="vocab-grid">
                `;
                
                topic.words.forEach(w => {
                    const wordClean = w.word.replace(/'/g, "\\'");
                    html += `
                        <div class="vocab-card" data-word="${w.word.toLowerCase()}" data-meaning="${w.meaning.toLowerCase()}">
                            <div class="vocab-header-row">
                                <span class="vocab-word">${w.word}</span>
                                <button class="btn-speak-vocab" onclick="window.speakWord('${wordClean}')" title="Nghe đọc mẫu">
                                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor">
                                        <path d="M12 3L6.5 8H2V16H6.5L12 21V3ZM16.5 12C16.5 10.23 15.48 8.71 14 8V16C15.48 15.29 16.5 13.77 16.5 12ZM14 3.23V5.29C16.89 6.15 19 8.83 19 12C19 15.17 16.89 17.85 14 18.71V20.77C18.01 19.86 21 16.28 21 12C21 7.72 18.01 4.14 14 3.23Z"/>
                                    </svg>
                                </button>
                                ${w.pos ? `<span class="vocab-pos">${w.pos}</span>` : ''}
                            </div>
                            ${w.ipa ? `<div class="vocab-ipa">${w.ipa}</div>` : ''}
                            <div class="vocab-meaning">${w.meaning}</div>
                        </div>
                    `;
                });
                
                html += `
                        </div>
                    </div>
                `;
            });
            
            container.innerHTML = html;
        });
        
        // Set up search filter listener
        const searchInput = document.getElementById('vocab-search');
        if (searchInput) {
            searchInput.addEventListener('input', (e) => {
                const query = e.target.value.toLowerCase().trim();
                const activePane = document.querySelector('#vocab-tab-body .tab-pane.active');
                if (!activePane) return;
                
                const topicBlocks = activePane.querySelectorAll('.vocab-topic-block');
                topicBlocks.forEach(block => {
                    const cards = block.querySelectorAll('.vocab-card');
                    let visibleCount = 0;
                    
                    cards.forEach(card => {
                        const word = card.getAttribute('data-word') || '';
                        const meaning = card.getAttribute('data-meaning') || '';
                        if (word.includes(query) || meaning.includes(query)) {
                            card.style.display = 'flex';
                            visibleCount++;
                        } else {
                            card.style.display = 'none';
                        }
                    });
                    
                    if (visibleCount > 0 || query === '') {
                        block.style.display = 'block';
                    } else {
                        block.style.display = 'none';
                    }
                });
            });
        }
    }

    /* --- PRACTICE RUN ENGINE --- */
    startPractice(partNum, id, isTheory = false) {
        if (!this.isItemUnlocked(partNum, id, isTheory)) {
            this.promptUnlock(partNum, id, isTheory, () => {
                this.startPractice(partNum, id, isTheory);
            });
            return;
        }

        // Set active session state
        this.activeSession.part = partNum;
        this.activeSession.id = id;
        this.activeSession.isTheory = isTheory;
        this.activeSession.userAnswers = {};
        this.activeSession.submitted = false;
        
        // Hide report card
        this.elements.practiceReportCard.classList.add('hidden');
        
        // Find corresponding data object
        let dataObj = null;
        if (isTheory) {
            dataObj = this.data.part1.theory.find(t => t.id === id);
        } else {
            const practices = this.data[`part${partNum}`].practice;
            dataObj = practices.find(p => p.id === id);
        }
        
        if (!dataObj) return;
        this.activeSession.data = dataObj;
        
        // Setup Player Info
        this.elements.playerTitle.textContent = dataObj.title;
        this.elements.playerPartBadge.textContent = isTheory ? "Lý thuyết" : `PART 0${partNum}`;
        this.elements.playerPartBadge.className = `audio-badge bg-${partNum === 1 ? 'purple' : partNum === 2 ? 'blue' : 'green'}`;
        
        // Setup Audio Source
        if (isTheory) {
            this.elements.mainPlayerCard.style.display = 'none';
        } else {
            this.elements.mainPlayerCard.style.display = 'block';
            this.elements.audio.src = dataObj.audio || "";
            this.stopAudio();
        }
        
        // Reset speed selector to 1x
        this.elements.audio.playbackRate = 1.0;
        this.elements.speedBtn.textContent = '1.00x';
        document.querySelectorAll('.speed-option').forEach(o => {
            o.classList.remove('active');
            if (o.getAttribute('data-speed') === '1.0') o.classList.add('active');
        });
        
        // Reset timeline slider UI
        this.elements.currentTimeText.textContent = '0:00';
        this.elements.totalTimeText.textContent = '0:00';
        this.elements.progressFill.style.width = '0%';
        this.elements.progressHandle.style.left = '0%';
        
        // Render Questions
        this.renderQuestions(dataObj);
        
        // Show/Hide practice footer button
        if (isTheory) {
            this.elements.submitBtn.style.display = 'none'; // Theory uses per-question submit
        } else {
            this.elements.submitBtn.style.display = 'block';
            this.elements.submitBtn.textContent = "ĐÁP ÁN & GIẢI THÍCH";
        }
        
        // Switch view
        window.location.hash = 'practice-run';
    }

    renderQuestions(dataObj) {
        // If it is theory, we display all examples. If practice, we display questions.
        const listContainer = this.elements.questionsList;
        listContainer.innerHTML = '';
        
        const items = this.activeSession.isTheory ? dataObj.examples : dataObj.questions;
        
        items.forEach((item, index) => {
            const card = document.createElement('div');
            card.className = 'question-card glass-card';
            card.id = `q-card-${item.number || index + 1}`;
            
            const qTitle = this.activeSession.isTheory ? `Ví dụ ${item.number}:` : `Câu hỏi ${item.number}:`;
            
            // Build options HTML
            const optionsHtml = item.options.map(opt => {
                return `
                    <div class="option-item" data-q-num="${item.number || index + 1}" data-letter="${opt.letter}">
                        <div class="option-circle">${opt.letter}</div>
                        <div class="option-text-wrapper">
                            <span class="option-text">${opt.text}</span>
                            ${opt.text_vi ? `<span class="option-text-vi">${opt.text_vi}</span>` : ''}
                        </div>
                    </div>
                `;
            }).join('');
            
            // Audio for Theory
            const audioHtml = (this.activeSession.isTheory && item.audio) ? `
                <div class="mini-audio-player-wrapper">
                    <audio controls src="${item.audio}" class="mini-native-audio"></audio>
                </div>
            ` : '';
            
            // Generate Useful Vocabulary HTML if available
            let usefulVocabHtml = '';
            if (item.vocabulary && item.vocabulary.length > 0) {
                const vocabListItems = item.vocabulary.map(v => {
                    const match = v.match(/^([^/(:]+)(.*)$/);
                    if (match) {
                        const wordPart = match[1].trim();
                        const restPart = match[2] || '';
                        return `
                            <div style="margin-bottom: 8px; display: flex; align-items: flex-start;">
                                <button class="btn-speak-vocab" onclick="window.speakWord('${wordPart.replace(/'/g, "\\'")}')" style="background: none; border: none; cursor: pointer; color: var(--color-primary); padding: 0; margin-right: 8px; transform: translateY(1px);" title="Nghe đọc mẫu">
                                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor">
                                        <path d="M12 3L6.5 8H2V16H6.5L12 21V3ZM16.5 12C16.5 10.23 15.48 8.71 14 8V16C15.48 15.29 16.5 13.77 16.5 12ZM14 3.23V5.29C16.89 6.15 19 8.83 19 12C19 15.17 16.89 17.85 14 18.71V20.77C18.01 19.86 21 16.28 21 12C21 7.72 18.01 4.14 14 3.23Z"/>
                                    </svg>
                                </button>
                                <div>
                                    - <strong>${wordPart}</strong> ${restPart}
                                </div>
                            </div>
                        `;
                    }
                    return `<div style="margin-bottom: 8px;">- ${v}</div>`;
                }).join('');
                
                usefulVocabHtml = `
                    <div class="useful-vocab-section" style="margin-top: 24px; padding-top: 16px; border-top: 1px dashed var(--color-primary-light);">
                        <h4 style="margin-bottom: 12px; font-size: 0.95rem; font-weight: bold; color: var(--color-primary);">TỪ VỰNG HỮU ÍCH</h4>
                        <div style="font-size: 0.9rem; line-height: 1.5; color: var(--text-color);">
                            ${vocabListItems}
                        </div>
                    </div>
                `;
            }

            // Inline Explanation Panel HTML
            const explanationHtml = `
                <div class="practice-explanation-panel collapsed" id="inline-explanation-${item.number || index + 1}">
                    <div class="drawer-tabs">
                        <button class="inline-tab-btn active" data-inline-tab="transcript">Lời thoại song ngữ</button>
                        <button class="inline-tab-btn" data-inline-tab="vocabulary">Từ vựng</button>
                    </div>
                    <div class="drawer-body" style="padding-top: 16px;">
                        <div class="drawer-pane active" data-pane="transcript">
                            <div class="transcript-layout">
                                <div class="transcript-column">
                                    <h4 class="column-title" style="margin-bottom: 8px; font-size: 0.9rem; font-weight: bold; color: var(--color-primary);">Tiếng Anh</h4>
                                    <div class="transcript-content text-en" id="inline-en-${item.number || index + 1}" style="font-size: 0.9rem;"></div>
                                </div>
                                <div class="transcript-column">
                                    <h4 class="column-title" style="margin-bottom: 8px; font-size: 0.9rem; font-weight: bold; color: var(--color-secondary);">Tiếng Việt</h4>
                                    <div class="transcript-content text-vi" id="inline-vi-${item.number || index + 1}" style="font-size: 0.9rem;"></div>
                                </div>
                            </div>
                            ${usefulVocabHtml}
                        </div>
                        <div class="drawer-pane" data-pane="vocabulary">
                            <div class="vocab-cards" id="inline-vocab-${item.number || index + 1}"></div>
                        </div>
                    </div>
                </div>
            `;
            
            const submitSingleBtn = this.activeSession.isTheory ? `
                <div style="margin-top: 16px; text-align: right;">
                    <button class="btn btn-primary btn-submit-single" data-q-num="${item.number || index + 1}">ĐÁP ÁN & GIẢI THÍCH</button>
                </div>
            ` : '';
            
            const qText = item.question ? item.question.replace(/^:\s*/, '') : '';
            const qTextVi = item.question_vi ? item.question_vi.replace(/^:\s*/, '') : '';
            
            const exampleLabelHtml = this.activeSession.isTheory ? `
                <span class="example-label">EXAMPLE ${String(item.number || index + 1).padStart(2, '0')}</span>
            ` : '';
            
            card.innerHTML = `
                ${exampleLabelHtml}
                ${audioHtml}
                <div class="question-header">
                    <div class="question-number">${item.number || index + 1}</div>
                    <div>
                        <div class="question-text">${qText}</div>
                        ${qTextVi ? `<div class="question-translation">${qTextVi}</div>` : ''}
                    </div>
                </div>
                <div class="options-list">
                    ${optionsHtml}
                </div>
                ${submitSingleBtn}
                ${explanationHtml}
            `;
            
            listContainer.appendChild(card);
        });
        
        // Add click events to option items
        document.querySelectorAll('.option-item').forEach(optItem => {
            optItem.addEventListener('click', (e) => {
                if (this.activeSession.submitted) return; // cannot change after submit
                
                const qNum = optItem.getAttribute('data-q-num');
                const letter = optItem.getAttribute('data-letter');
                
                // Toggle active class on option siblings
                const card = optItem.closest('.question-card');
                card.querySelectorAll('.option-item').forEach(item => {
                    item.classList.remove('selected');
                });
                optItem.classList.add('selected');
                
                // Save selection state
                this.activeSession.userAnswers[qNum] = letter;
            });
        });
    }

    submitPractice() {
        const isTheory = this.activeSession.isTheory;
        const dataObj = this.activeSession.data;
        const items = isTheory ? dataObj.examples : dataObj.questions;
        
        // If not theory, make sure at least one answer is selected (or warn, but allow anyway)
        const totalQuestions = items.length;
        
        // Mark session as submitted
        this.activeSession.submitted = true;
        this.stopAudio();
        
        // Validate each question
        let correctCount = 0;
        
        items.forEach((item, index) => {
            const qNum = item.number || index + 1;
            const userAns = this.activeSession.userAnswers[qNum];
            const correctAns = item.correct;
            const card = document.getElementById(`q-card-${qNum}`);
            
            if (userAns === correctAns) {
                correctCount++;
            }
            
            // Ensure translations are shown even if unanswered
            card.classList.add('show-translations');
            
            // Mark option styles
            card.querySelectorAll('.option-item').forEach(opt => {
                const letter = opt.getAttribute('data-letter');
                
                // Remove selection visual class
                opt.classList.remove('selected');
                
                // Show green for correct answer
                if (letter === correctAns) {
                    opt.classList.add('validated-correct');
                }
                // Show red for wrong user selection
                if (letter === userAns && userAns !== correctAns) {
                    opt.classList.add('validated-incorrect');
                }
            });
        });
        
        // Save progress & history
        if (isTheory) {
            this.progress.completedTheory[dataObj.id] = true;
            this.saveProgress();
            this.renderLists();
        } else {
            // Save test score
            // Keep the highest score if already taken
            const prevScore = this.progress.completedTests[dataObj.id];
            if (prevScore === undefined || correctCount > prevScore) {
                this.progress.completedTests[dataObj.id] = correctCount;
            }
            
            // Append history entry
            const sessionName = `${dataObj.part === 1 ? 'PART 01' : dataObj.part === 2 ? 'PART 02' : 'PART 03'} - ${dataObj.title}`;
            this.progress.history.unshift({
                timestamp: new Date().toLocaleString('vi-VN'),
                part: dataObj.part,
                title: dataObj.title,
                score: `${correctCount} / ${totalQuestions}`,
                percent: Math.round((correctCount / totalQuestions) * 100)
            });
            
            this.saveProgress();
            this.renderLists();
            this.renderHistory();

            // Display and populate practice report card
            this.elements.reportStudentName.textContent = this.studentName || "Chưa nhập tên";
            this.elements.reportTestTitle.textContent = `${dataObj.part === 1 ? 'PART 01' : dataObj.part === 2 ? 'PART 02' : 'PART 03'} - ${dataObj.title}`;
            this.elements.reportScore.textContent = `${correctCount} / ${totalQuestions} câu đúng`;
            this.elements.reportAccuracy.textContent = `${Math.round((correctCount / totalQuestions) * 100)}%`;
            this.elements.practiceReportCard.classList.remove('hidden');
        }
        
        // Populate and show inline explanations
        this.populateInlineExplanations(dataObj);
        this.updateStats();
    }
    
    submitSingleTheoryItem(qNum) {
        const dataObj = this.activeSession.data;
        const item = dataObj.examples.find(ex => (ex.number || dataObj.examples.indexOf(ex) + 1) == qNum);
        if (!item) return;
        
        const userAns = this.activeSession.userAnswers[qNum];
        const correctAns = item.correct;
        const card = document.getElementById(`q-card-${qNum}`);
        
        // Ensure translations are shown
        card.classList.add('show-translations');
        
        // Mark option styles
        card.querySelectorAll('.option-item').forEach(opt => {
            const letter = opt.getAttribute('data-letter');
            opt.classList.remove('selected');
            if (letter === correctAns) {
                opt.classList.add('validated-correct');
            }
            if (letter === userAns && userAns !== correctAns) {
                opt.classList.add('validated-incorrect');
            }
        });
        
        // Mark as submitted for this specific question
        // Prevent further clicks by disabling pointer events on options
        card.querySelectorAll('.option-item').forEach(opt => opt.style.pointerEvents = 'none');
        
        // Populate and show its inline explanation
        this.populateInlineExplanations(dataObj, qNum);
        
        // Hide the single submit button
        const btn = card.querySelector('.btn-submit-single');
        if (btn) btn.style.display = 'none';
        
        // We do not save progress until all examples are done? 
        // Actually for simplicity, we can just mark theory as completed when they open at least one explanation.
        this.progress.completedTheory[dataObj.id] = true;
        this.saveProgress();
        this.renderLists();
    }

    parseVocabItem(item) {
        let word = item;
        let ipa = "";
        let pos = "";
        let meaning = "";
        
        const m_ipa = item.match(/([^\/]+)\s*\/([^\/]+)\/\s*(.*)/);
        if (m_ipa) {
            word = m_ipa[1].trim();
            ipa = `/${m_ipa[2]}/`;
            const remainder = m_ipa[3];
            const m_pos = remainder.match(/\(([^)]+)\)\s*:\s*(.*)/);
            if (m_pos) {
                pos = `(${m_pos[1]})`;
                meaning = m_pos[2];
            } else {
                meaning = remainder.replace(/^:\s*/, '');
            }
        } else {
            const m_colon = item.match(/([^:]+):\s*(.*)/);
            if (m_colon) {
                word = m_colon[1];
                meaning = m_colon[2];
            }
        }
        
        return `
            <div class="vocab-card">
                <span class="vocab-word">${word}</span>
                ${ipa ? `<span class="vocab-ipa">${ipa}</span>` : ''}
                ${pos ? `<span class="vocab-pos">${pos}</span>` : ''}
                <span class="vocab-meaning">${meaning}</span>
            </div>
        `;
    }

    cleanTranscriptLine(line) {
        if (!line) return "";
        
        // 1. Extract speakers/numbers from the START of a highlight span
        line = line.replace(/<span class="highlight">\s*(M:|W:|Nam:|Nữ:|Man:|Woman:|\(\d+\))\s*/gi, '<strong>$1</strong> <span class="highlight">');
        
        // 2. Remove any highlight spans that only contain whitespace
        line = line.replace(/<span class="highlight">\s*<\/span>/g, ' ');
        
        // 3. Bold any speakers that are at the very start of the line (or after a quote)
        line = line.replace(/^(M:|W:|Nam:|Nữ:|Man:|Woman:)\s*/gi, '<strong>$1</strong> ');
        
        // 4. Clean up multiple spaces
        line = line.replace(/\s{2,}/g, ' ');
        
        return line.trim();
    }

    populateInlineExplanations(dataObj, singleQuestionNum = null) {
        const items = this.activeSession.isTheory ? dataObj.examples : dataObj.questions;
        
        // If Part 2 or 3 Practice, transcript and vocab are at the root level
        const isRootTranscript = !this.activeSession.isTheory && (this.activeSession.part === 2 || this.activeSession.part === 3);
        
        let rootEnHtml = "";
        let rootViHtml = "";
        let rootVocabList = [];
        
        if (isRootTranscript) {
            if (dataObj.en_transcript) rootEnHtml = dataObj.en_transcript.map(line => `<p style="margin-bottom:10px;">${this.cleanTranscriptLine(line)}</p>`).join('');
            if (dataObj.vi_transcript) rootViHtml = dataObj.vi_transcript.map(line => `<p style="margin-bottom:10px; font-style:italic;">${this.cleanTranscriptLine(line)}</p>`).join('');
            if (dataObj.vocabulary) rootVocabList = dataObj.vocabulary;
        }
        
        items.forEach((item, index) => {
            const qNum = item.number || index + 1;
            
            // If we are only updating a single question (Theory Example submit)
            if (singleQuestionNum !== null && qNum != singleQuestionNum) return;
            
            let enHtml = "";
            let viHtml = "";
            let vocabList = [];
            
            if (isRootTranscript) {
                enHtml = rootEnHtml;
                viHtml = rootViHtml;
                vocabList = rootVocabList;
            } else {
                if (item.en_transcript) enHtml = item.en_transcript.map(line => `<p style="margin-bottom:10px;">${this.cleanTranscriptLine(line)}</p>`).join('');
                if (item.vi_transcript) viHtml = item.vi_transcript.map(line => `<p style="margin-bottom:10px; font-style:italic;">${this.cleanTranscriptLine(line)}</p>`).join('');
                if (item.vocabulary) vocabList = item.vocabulary;
            }
            
            const enContainer = document.getElementById(`inline-en-${qNum}`);
            const viContainer = document.getElementById(`inline-vi-${qNum}`);
            const vocabContainer = document.getElementById(`inline-vocab-${qNum}`);
            const panel = document.getElementById(`inline-explanation-${qNum}`);
            
            if (enContainer) enContainer.innerHTML = enHtml;
            if (viContainer) viContainer.innerHTML = viHtml;
            
            if (vocabContainer) {
                if (vocabList && vocabList.length > 0) {
                    vocabContainer.innerHTML = vocabList.map(v => this.parseVocabItem(v)).join('');
                } else {
                    vocabContainer.innerHTML = '<p class="text-secondary">Không có từ vựng nổi bật.</p>';
                }
            }
            
            // Uncollapse the panel
            if (panel) {
                panel.classList.remove('collapsed');
            }
        });
    }

    exitPractice() {
        this.stopAudio();
        // Switch back to calling part panel
        const part = this.activeSession.part || 1;
        window.location.hash = `part${part}`;
    }

    /* --- AUDIO PLAYER HELPER METHODS --- */
    toggleAudio() {
        if (this.audioPlaying) {
            this.pauseAudio();
        } else {
            this.playAudio();
        }
    }

    playAudio() {
        this.elements.audio.play();
        this.setAudioState(true);
    }

    pauseAudio() {
        this.elements.audio.pause();
        this.setAudioState(false);
    }

    stopAudio() {
        this.elements.audio.pause();
        this.elements.audio.currentTime = 0;
        this.setAudioState(false);
    }

    setAudioState(isPlaying) {
        this.audioPlaying = isPlaying;
        if (isPlaying) {
            this.elements.playBtn.querySelector('.icon-play').classList.add('hidden');
            this.elements.playBtn.querySelector('.icon-pause').classList.remove('hidden');
        } else {
            this.elements.playBtn.querySelector('.icon-play').classList.remove('hidden');
            this.elements.playBtn.querySelector('.icon-pause').classList.add('hidden');
        }
    }

    formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = Math.floor(seconds % 60);
        return `${mins}:${secs < 10 ? '0' : ''}${secs}`;
    }

    /* --- THEME MANAGER --- */
    loadTheme() {
        const savedTheme = localStorage.getItem('vstep-theme') || 'dark';
        document.documentElement.setAttribute('data-theme', savedTheme);
    }

    toggleTheme() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('vstep-theme', newTheme);
    }

    /* --- PROGRESS & LOCAL STORAGE --- */
    loadProgress() {
        const savedProgress = localStorage.getItem('vstep-listening-progress');
        if (savedProgress) {
            try {
                const parsed = JSON.parse(savedProgress);
                this.progress = {
                    completedTests: parsed.completedTests || {},
                    completedTheory: parsed.completedTheory || {},
                    history: parsed.history || []
                };
            } catch (e) {
                console.error("Error parsing saved progress:", e);
            }
        }
        this.renderHistory();
    }

    saveProgress() {
        localStorage.setItem('vstep-listening-progress', JSON.stringify(this.progress));
    }

    clearProgress() {
        if (confirm("Bạn có chắc chắn muốn xóa toàn bộ lịch sử và tiến độ học tập không?")) {
            this.progress = {
                completedTests: {},
                completedTheory: {},
                history: []
            };
            this.saveProgress();
            this.renderLists();
            this.renderHistory();
            this.updateStats();
            alert("Đã xóa tiến độ thành công!");
        }
    }

    updateStats() {
        // Calculate progress stats
        const totalTheory = 6;
        const totalTests = 17; // Part 1 (4) + Part 2 (8) + Part 3 (5)
        
        const theoryCompleted = Object.keys(this.progress.completedTheory).length;
        const testsCompleted = Object.keys(this.progress.completedTests).length;
        
        // Calculate accuracy
        let totalScore = 0;
        let totalPossible = 0;
        
        // Part 1 completed scores
        // We know score is stored as correct answers count.
        // Part 1 tests have 8 questions.
        // Part 2 tests have 4 questions.
        // Part 3 tests have 5 questions.
        for (const [testId, score] of Object.entries(this.progress.completedTests)) {
            let possible = 8;
            if (testId.startsWith('p2_')) possible = 4;
            if (testId.startsWith('p3_')) possible = 5;
            
            totalScore += score;
            totalPossible += possible;
        }
        
        const accuracy = totalPossible > 0 ? Math.round((totalScore / totalPossible) * 100) : 0;
        
        // Update stats DOM
        this.elements.statsTheory.textContent = `${theoryCompleted} / ${totalTheory}`;
        this.elements.statsTests.textContent = `${testsCompleted} / ${totalTests}`;
        this.elements.statsAccuracy.textContent = `${accuracy}%`;
        
        // Update header progress bar
        const totalProgressPercent = Math.round(((theoryCompleted + testsCompleted) / (totalTheory + totalTests)) * 100);
        this.elements.overallProgressFill.style.width = `${totalProgressPercent}%`;
        this.elements.overallProgressText.textContent = `${totalProgressPercent}%`;
    }

    renderHistory() {
        const body = this.elements.statsTableBody;
        
        if (this.progress.history.length === 0) {
            body.innerHTML = `
                <tr>
                    <td colspan="6" class="empty-state">Chưa có dữ liệu tiến độ làm bài nào được lưu. Hãy làm một bài nghe để bắt đầu ghi nhận!</td>
                </tr>
            `;
            return;
        }
        
        body.innerHTML = this.progress.history.map(entry => {
            return `
                <tr>
                    <td>${entry.timestamp}</td>
                    <td><strong>PART 0${entry.part}</strong></td>
                    <td>${entry.title}</td>
                    <td><strong>${entry.score}</strong></td>
                    <td>
                        <span style="color: ${entry.percent >= 80 ? 'var(--color-success)' : entry.percent >= 50 ? 'var(--color-secondary)' : 'var(--color-error)'}">
                            ${entry.percent}%
                        </span>
                    </td>
                    <td>
                        <button class="btn btn-secondary" style="padding:4px 10px; font-size:0.75rem;" onclick="app.startPractice(${entry.part}, '${entry.part === 1 ? 'p1' : entry.part === 2 ? 'p2' : 'p3'}_practice_${entry.title.split(' ')[1]}', false)">
                            Làm lại
                        </button>
                    </td>
                </tr>
            `;
        }).join('');
    }

    normalizeNameAndClass(inputName) {
        if (!inputName) return "";
        // Standardize any dash, colon, or slash and surrounding spaces to a clean ' - ' format
        return inputName.replace(/\s*[\-\–\—:\/]\s*/g, ' - ').trim();
    }

    checkStudentName() {
        const studentName = this.studentName;
        // Validate if the stored name contains a hyphen separating Name and Class
        let hasValidFormat = studentName && studentName.includes(' - ') && studentName.trim() !== "Học viên VSTEP";
        
        if (hasValidFormat) {
            const parts = studentName.split(' - ');
            const studentClass = parts[1] ? parts[1].trim().toUpperCase() : '';
            if (!this.allowedClasses.includes(studentClass)) {
                hasValidFormat = false;
            }
        }
        
        if (!studentName || !hasValidFormat) {
            if (this.elements.studentNameInput) this.elements.studentNameInput.value = "";
            if (this.elements.studentClassInput) this.elements.studentClassInput.value = "";
            this.elements.welcomeModal.classList.remove('hidden');
        } else {
            this.elements.welcomeModal.classList.add('hidden');
            this.updateSidebarUser(studentName);
        }
    }

    saveStudentName() {
        const inputName = this.elements.studentNameInput.value.trim();
        const inputClass = this.elements.studentClassInput.value.trim().toUpperCase();
        
        if (!this.allowedClasses.includes(inputClass)) {
            alert(`Lớp học "${inputClass}" không hợp lệ!\nVui lòng nhập đúng tên lớp được cấp (Ví dụ: ONB103, CB206, CB210, CB211, CB213, B212)`);
            return;
        }
        
        if (inputName && inputClass) {
            const combined = `${inputName} - ${inputClass}`;
            this.studentName = combined;
            sessionStorage.setItem('vstep_student_name', combined);
            this.checkStudentName();
            this.submitToGoogleForm(combined);
        }
    }

    editStudentName() {
        const parts = this.studentName.split(' - ');
        const currentName = parts[0] || "";
        const currentClass = parts[1] || "";
        
        const newName = prompt("Nhập họ tên mới (Ví dụ: Phạm Minh Nguyệt):", currentName);
        if (newName === null) return;
        
        const newClass = prompt("Nhập lớp học mới (Ví dụ: ONB103):", currentClass);
        if (newClass === null) return;
        
        const nameVal = newName.trim();
        const classVal = newClass.trim().toUpperCase();
        
        if (!this.allowedClasses.includes(classVal)) {
            alert(`Lớp học "${classVal}" không hợp lệ!\nVui lòng nhập đúng tên lớp được cấp (Ví dụ: ONB103, CB206, CB210, CB211, CB213, B212)`);
            return;
        }
        
        if (nameVal && classVal) {
            const combined = `${nameVal} - ${classVal}`;
            this.studentName = combined;
            sessionStorage.setItem('vstep_student_name', combined);
            this.updateSidebarUser(combined);
            this.submitToGoogleForm(combined);
            alert("Đã cập nhật thông tin học viên!");
        }
    }

    updateSidebarUser(name) {
        if (this.elements.sidebarUserName) {
            this.elements.sidebarUserName.textContent = name;
        }
        if (this.elements.userAvatarChar) {
            this.elements.userAvatarChar.textContent = name.charAt(0).toUpperCase();
        }
    }

    submitToGoogleForm(nameAndClass) {
        const url = 'https://docs.google.com/forms/d/e/1FAIpQLSdpfOuY9nxxUmdF2UsW2UONZm4SsolHrViqNGyF3NqS62CNSA/formResponse';
        
        // Use URLSearchParams for application/x-www-form-urlencoded payload
        const formData = new URLSearchParams();
        formData.append('entry.388968236', nameAndClass);
        
        // Perform background submit via fetch with mode: 'no-cors'
        fetch(url, {
            method: 'POST',
            mode: 'no-cors',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: formData.toString()
        })
        .then(() => {
            console.log("Submitted to Google Form successfully via fetch:", nameAndClass);
        })
        .catch(err => {
            console.error("Google Form submission failed:", err);
        });
    }

    sendReportToTeacher() {
        const studentName = this.studentName || "Học viên ẩn danh";
        const dataObj = this.activeSession.data;
        const isTheory = this.activeSession.isTheory;
        
        let correctCount = 0;
        const items = isTheory ? dataObj.examples : dataObj.questions;
        const totalQuestions = items.length;
        
        items.forEach((item, index) => {
            const qNum = item.number || index + 1;
            const userAns = this.activeSession.userAnswers[qNum];
            const correctAns = item.correct;
            if (userAns === correctAns) {
                correctCount++;
            }
        });
        
        const accuracy = Math.round((correctCount / totalQuestions) * 100);
        const partText = dataObj.part === 1 ? "PART 01" : dataObj.part === 2 ? "PART 02" : "PART 03";
        const reportText = `[BÁO CÁO KẾT QUẢ BÀI LÀM]
Học viên & Lớp: ${studentName}
Bài học: ${partText} - ${dataObj.title}
Kết quả: ${correctCount} / ${totalQuestions} câu đúng (${accuracy}%)
Thời gian nộp: ${new Date().toLocaleString('vi-VN')}`;
        
        navigator.clipboard.writeText(reportText).then(() => {
            alert("Đã sao chép báo cáo vào khay nhớ tạm!\nHệ thống sẽ chuyển bạn sang trang Facebook River English Center để gửi báo cáo.");
            window.open("https://www.facebook.com/anhnguRiverCT", "_blank");
        }).catch(err => {
            console.error("Could not copy text: ", err);
            alert("Không thể tự động sao chép báo cáo. Vui lòng sao chép thủ công:\n\n" + reportText);
            window.open("https://www.facebook.com/anhnguRiverCT", "_blank");
        });
    }

    exportCumulativeReport() {
        const studentName = this.studentName || "Học viên ẩn danh";
        if (!this.progress.history || this.progress.history.length === 0) {
            alert("Chưa có dữ liệu tiến độ làm bài nào để xuất báo cáo!");
            return;
        }
        
        let reportText = `[BÁO CÁO TỔNG HỢP KẾT QUẢ HỌC TẬP]
Học viên & Lớp: ${studentName}
Thời gian xuất báo cáo: ${new Date().toLocaleString('vi-VN')}
---------------------------------------------
Danh sách bài đã làm:
`;

        this.progress.history.forEach((entry, idx) => {
            reportText += `\n${idx + 1}. ${entry.timestamp} | PART 0${entry.part} - ${entry.title} | Kết quả: ${entry.score} (${entry.percent}%)`;
        });
        
        reportText += `\n\n---------------------------------------------\nTổng cộng đã làm: ${this.progress.history.length} bài.`;
        
        navigator.clipboard.writeText(reportText).then(() => {
            alert("Đã sao chép báo cáo tổng hợp vào khay nhớ tạm!\nHệ thống sẽ chuyển bạn sang trang Facebook River English Center để gửi báo cáo.");
            window.open("https://www.facebook.com/anhnguRiverCT", "_blank");
        }).catch(err => {
            console.error("Could not copy text: ", err);
            alert("Không thể tự động sao chép báo cáo tổng hợp. Vui lòng sao chép thủ công:\n\n" + reportText);
            window.open("https://www.facebook.com/anhnguRiverCT", "_blank");
        });
    }
}

// Global App instance helper helper methods
String.prototype.strip = function() {
    return this.trim();
};

const app = new VstepApp();

window.speakWord = (word) => {
    if ('speechSynthesis' in window) {
        window.speechSynthesis.cancel();
        let cleanWord = word.split('/')[0].split(',')[0].trim();
        cleanWord = cleanWord.replace(/\([^)]*\)/g, '').trim();
        cleanWord = cleanWord.replace(/[^\w\s\-]/g, '').trim();
        
        const utterance = new SpeechSynthesisUtterance(cleanWord);
        utterance.lang = 'en-US';
        
        // Prioritize natural-sounding, younger conversational US voices
        const voices = window.speechSynthesis.getVoices();
        const priorities = ["Google US English", "Ava", "Allison", "Siri", "Samantha", "Victoria"];
        let selectedVoice = null;
        
        for (const name of priorities) {
            const found = voices.find(v => v.name.includes(name) && v.lang.startsWith('en'));
            if (found) {
                selectedVoice = found;
                break;
            }
        }
        
        if (!selectedVoice) {
            selectedVoice = voices.find(v => v.lang === 'en-US' || v.lang === 'en_US') || 
                            voices.find(v => v.lang.startsWith('en'));
        }
        
        if (selectedVoice) {
            utterance.voice = selectedVoice;
        }
        
        utterance.pitch = 1.05; // Slightly higher pitch for a younger, friendlier voice
        utterance.rate = 0.92;  // Natural conversational speed (not robotic or excessively slow)
        window.speechSynthesis.speak(utterance);
    } else {
        alert("Trình duyệt của bạn không hỗ trợ tính năng phát âm.");
    }
};

// ==========================================================
// VOCABULARY REVIEW GAMES SYSTEM
// ==========================================================

let audioCtx = null;
function playTone(freq, type, duration) {
    try {
        const AC = window.AudioContext || window.webkitAudioContext;
        if (!AC) return;
        if (!audioCtx) {
            audioCtx = new AC();
        }
        if (audioCtx.state === 'suspended') audioCtx.resume();
        const osc = audioCtx.createOscillator();
        const gain = audioCtx.createGain();
        osc.type = type;
        osc.frequency.setValueAtTime(freq, audioCtx.currentTime);
        gain.gain.setValueAtTime(0.08, audioCtx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + duration);
        osc.connect(gain);
        gain.connect(audioCtx.destination);
        osc.start();
        osc.stop(audioCtx.currentTime + duration);
    } catch (e) {
        console.error("sfx error:", e);
    }
}

const sfx = {
    flip: () => playTone(300, 'sine', 0.1),
    correct: () => {
        playTone(600, 'sine', 0.1);
        setTimeout(() => playTone(800, 'sine', 0.15), 100);
    },
    wrong: () => {
        playTone(250, 'sawtooth', 0.2);
        setTimeout(() => playTone(200, 'sawtooth', 0.25), 100);
    },
    win: () => {
        playTone(400, 'sine', 0.1);
        setTimeout(() => playTone(500, 'sine', 0.1), 100);
        setTimeout(() => playTone(600, 'sine', 0.1), 200);
        setTimeout(() => playTone(800, 'sine', 0.4), 300);
    }
};

function shootConfetti() {
    if (typeof confetti === 'function') {
        const duration = 2500;
        const end = Date.now() + duration;
        (function frame() {
            confetti({ particleCount: 3, angle: 60, spread: 55, origin: { x: 0 }, colors: ['#26ccff', '#a25afd', '#ff5e7e', '#88ff5a', '#fcff42', '#ffa62d', '#ff36ff'], zIndex: 9999 });
            confetti({ particleCount: 3, angle: 120, spread: 55, origin: { x: 1 }, colors: ['#26ccff', '#a25afd', '#ff5e7e', '#88ff5a', '#fcff42', '#ffa62d', '#ff36ff'], zIndex: 9999 });
            if (Date.now() < end) requestAnimationFrame(frame);
        }());
    }
}

window.startReviewGame = (type) => {
    const activeBtn = document.querySelector('#vocab-tab-header .tab-btn.active');
    if (!activeBtn) return;
    const tabId = activeBtn.getAttribute('data-tab');
    const catIdx = parseInt(tabId.split('-')[2]);
    
    if (!window.VSTEP_VOCAB_DATA || !window.VSTEP_VOCAB_DATA[catIdx]) {
        alert("Không tìm thấy dữ liệu từ vựng cho phần này!");
        return;
    }
    
    const catData = window.VSTEP_VOCAB_DATA[catIdx];
    const gameWords = [];
    catData.topics.forEach(topic => {
        topic.words.forEach(w => {
            gameWords.push({
                en: w.word.trim(),
                vn: w.meaning.trim()
            });
        });
    });
    
    if (gameWords.length === 0) {
        alert("Chưa có từ vựng nào trong danh mục này để chơi!");
        return;
    }
    
    const placeholder = document.getElementById('game-placeholder');
    const content = document.getElementById('game-content');
    
    if (placeholder) placeholder.style.display = 'none';
    if (content) {
        content.style.display = 'block';
        content.innerHTML = '';
    }
    
    if (type === 'flashcards') {
        initFlashcards(gameWords, content);
    } else if (type === 'matching') {
        initMatchingGame(gameWords, content);
    } else if (type === 'quiz') {
        initQuizGame(gameWords, content);
    } else if (type === 'spelling') {
        initSpellingGame(gameWords, content);
    }
};

function initFlashcards(allWords, container) {
    let words = [...allWords].sort(() => 0.5 - Math.random());
    let currentIndex = 0;
    
    function renderCard() {
        if (currentIndex >= words.length) {
            sfx.win();
            shootConfetti();
            container.innerHTML = `
                <div style="text-align:center; padding: 32px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                    <div style="font-size: 4rem; margin-bottom: 16px;">🏆</div>
                    <h3 style="font-size:1.4rem; margin-bottom:16px; font-weight:800; color: var(--color-primary);">Tuyệt vời! Bạn đã hoàn thành tất cả các thẻ.</h3>
                    <button class="btn btn-primary" onclick="window.startReviewGame('flashcards')">🔄 Ôn tập lại</button>
                </div>
            `;
            return;
        }
        
        const word = words[currentIndex];
        const cleanWord = word.en.replace(/'/g, "\\'");
        
        container.innerHTML = `
            <div style="display:flex; flex-direction:column; align-items:center; width:100%; justify-content:center;">
                <div style="margin-bottom:12px; font-weight:bold; color:var(--text-muted);">Thẻ ${currentIndex + 1} / ${words.length}</div>
                <div class="flashcard-container" onclick="
                    const card = this.querySelector('.flashcard');
                    if (!card.classList.contains('flipped')) {
                        sfx.flip();
                        card.classList.add('flipped');
                        window.speakWord('${cleanWord}');
                    } else {
                        card.classList.remove('flipped');
                    }
                ">
                    <div class="flashcard">
                        <div class="flashcard-face flashcard-front">
                            <div class="fc-word">${word.en}</div>
                            <div class="fc-hint">👆 Nhấp để xem nghĩa tiếng Việt</div>
                        </div>
                        <div class="flashcard-face flashcard-back">
                            <div class="fc-word">${word.vn}</div>
                            <div class="fc-hint">🔊 Nhấp để nghe lại phát âm</div>
                        </div>
                    </div>
                </div>
                <div style="display:flex; gap:16px; margin-top:8px; flex-wrap:wrap; justify-content:center; width:100%;">
                    <button class="btn" style="background:#fef2f2; color:#991b1b; border:1px solid #fecaca; box-shadow:none; padding:10px 20px;" id="fc-btn-review">❌ Cần ôn lại</button>
                    <button class="btn" style="background:#ecfdf5; color:#065f46; border:1px solid #a7f3d0; box-shadow:none; padding:10px 20px;" id="fc-btn-gotit">✅ Đã thuộc</button>
                </div>
            </div>
        `;
        
        document.getElementById('fc-btn-review').onclick = (e) => {
            e.stopPropagation();
            words.push(word);
            currentIndex++;
            renderCard();
        };
        
        document.getElementById('fc-btn-gotit').onclick = (e) => {
            e.stopPropagation();
            currentIndex++;
            renderCard();
        };
    }
    
    renderCard();
}

function initMatchingGame(allWords, container) {
    let pool = [...allWords].sort(() => 0.5 - Math.random()).slice(0, 6);
    let items = [];
    pool.forEach((w, i) => {
        items.push({ id: i, text: w.en, type: 'en', word: w });
        items.push({ id: i, text: w.vn, type: 'vn', word: w });
    });
    items.sort(() => 0.5 - Math.random());
    
    container.innerHTML = `
        <div style="display:flex; justify-content:space-between; margin-bottom:20px; align-items:center; flex-wrap:wrap; gap:12px; width:100%;">
            <div style="font-weight:bold; color:var(--text-primary); font-size:1.05rem;">🔗 Ghép các cặp từ tương ứng:</div>
            <button class="btn btn-secondary" onclick="window.startReviewGame('matching')" style="padding: 6px 12px; font-size: 0.85rem;">🔄 Bài mới</button>
        </div>
        <div class="matching-grid" id="match-grid"></div>
    `;
    
    const grid = document.getElementById('match-grid');
    let selectedItem = null;
    let matchedCount = 0;
    let animating = false;
    
    items.forEach((item, idx) => {
        const card = document.createElement('div');
        card.className = 'match-card';
        card.textContent = item.text;
        
        card.onclick = () => {
            if (animating || card.classList.contains('matched') || card.classList.contains('selected')) return;
            
            if (!selectedItem) {
                card.classList.add('selected');
                selectedItem = { el: card, data: item };
                if (item.type === 'en') window.speakWord(item.text);
            } else {
                animating = true;
                if (selectedItem.data.id === item.id && selectedItem.data.type !== item.type) {
                    card.classList.add('selected');
                    sfx.correct();
                    if (item.type === 'en') window.speakWord(item.text);
                    
                    setTimeout(() => {
                        card.classList.remove('selected');
                        card.classList.add('matched');
                        selectedItem.el.classList.remove('selected');
                        selectedItem.el.classList.add('matched');
                        selectedItem = null;
                        matchedCount++;
                        animating = false;
                        
                        if (matchedCount === 6) {
                            sfx.win();
                            shootConfetti();
                            setTimeout(() => {
                                container.innerHTML = `
                                    <div style="text-align:center; padding: 32px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                                        <div style="font-size: 4rem; margin-bottom: 16px;">🌟</div>
                                        <h3 style="font-size:1.4rem; margin-bottom:16px; font-weight:800; color: var(--color-primary);">Hoàn thành xuất sắc!</h3>
                                        <button class="btn btn-primary" onclick="window.startReviewGame('matching')">▶️ Chơi tiếp</button>
                                    </div>
                                `;
                            }, 300);
                        }
                    }, 400);
                } else {
                    card.classList.add('error');
                    selectedItem.el.classList.remove('selected');
                    selectedItem.el.classList.add('error');
                    sfx.wrong();
                    if (item.type === 'en') window.speakWord(item.text);
                    
                    setTimeout(() => {
                        card.classList.remove('error');
                        selectedItem.el.classList.remove('error');
                        selectedItem = null;
                        animating = false;
                    }, 500);
                }
            }
        };
        grid.appendChild(card);
    });
}

function initQuizGame(allWords, container) {
    let words = [...allWords].sort(() => 0.5 - Math.random()).slice(0, 10);
    let currentIndex = 0;
    let score = 0;
    
    function renderQuiz() {
        if (currentIndex >= words.length) {
            sfx.win();
            shootConfetti();
            container.innerHTML = `
                <div style="text-align:center; padding: 32px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                    <div style="font-size: 4rem; margin-bottom: 16px;">🏅</div>
                    <h3 style="font-size:1.4rem; margin-bottom:8px; font-weight:800; color: var(--color-primary);">Hoàn thành Trắc nghiệm!</h3>
                    <p style="font-size:1.15rem; margin-bottom:16px; color: var(--text-secondary);">Bạn đạt <strong style="color:var(--color-primary); font-size:1.4rem;">${score} / ${words.length}</strong> điểm.</p>
                    <button class="btn btn-primary" onclick="window.startReviewGame('quiz')">🔄 Làm lại</button>
                </div>
            `;
            return;
        }
        
        const currentWord = words[currentIndex];
        let options = [currentWord];
        let distractors = [...allWords].filter(w => w.en !== currentWord.en).sort(() => 0.5 - Math.random()).slice(0, 3);
        options = [...options, ...distractors].sort(() => 0.5 - Math.random());
        
        container.innerHTML = `
            <div class="quiz-container">
                <div style="display:flex; justify-content:space-between; margin-bottom:16px; color:var(--text-muted); font-weight:600;">
                    <div>Câu hỏi: <span style="color:var(--text-primary);">${currentIndex + 1} / ${words.length}</span></div>
                    <div>Điểm số: <span style="color:var(--color-primary);">${score}</span></div>
                </div>
                <div class="quiz-question">
                    Nghĩa tiếng Anh của từ:<br>
                    <span style="color:var(--text-primary); font-size:1.5rem; display:block; margin-top:8px; font-weight:800;">"${currentWord.vn}"</span>
                </div>
                <div class="quiz-options">
                    ${options.map((opt, i) => `
                        <div class="quiz-option" data-ans="${opt.en === currentWord.en}">
                            <div style="background:var(--border-color); border-radius:50%; width:28px; height:28px; display:flex; align-items:center; justify-content:center; flex-shrink:0; font-size:0.85rem; font-weight:800; color:var(--text-secondary);">${['A', 'B', 'C', 'D'][i]}</div>
                            <div>${opt.en}</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        const opts = container.querySelectorAll('.quiz-option');
        let answered = false;
        opts.forEach(opt => {
            opt.onclick = () => {
                if (answered) return;
                answered = true;
                const isCorrect = opt.getAttribute('data-ans') === 'true';
                window.speakWord(opt.querySelector('div:nth-child(2)').textContent);
                
                if (isCorrect) {
                    opt.classList.add('correct');
                    sfx.correct();
                    score++;
                } else {
                    opt.classList.add('wrong');
                    sfx.wrong();
                    opts.forEach(o => {
                        if (o.getAttribute('data-ans') === 'true') o.classList.add('correct');
                    });
                }
                
                setTimeout(() => {
                    currentIndex++;
                    renderQuiz();
                }, 1500);
            };
        });
    }
    
    renderQuiz();
}

function initSpellingGame(allWords, container) {
    let words = [...allWords].sort(() => 0.5 - Math.random()).slice(0, 10);
    let currentIndex = 0;
    let score = 0;
    
    function renderSpelling() {
        if (currentIndex >= words.length) {
            sfx.win();
            shootConfetti();
            container.innerHTML = `
                <div style="text-align:center; padding: 32px; display: flex; flex-direction: column; align-items: center; justify-content: center; width: 100%;">
                    <div style="font-size: 4rem; margin-bottom: 16px;">⌨️</div>
                    <h3 style="font-size:1.4rem; margin-bottom:8px; font-weight:800; color: var(--color-primary);">Hoàn thành Thử thách gõ từ!</h3>
                    <p style="font-size:1.15rem; margin-bottom:16px; color: var(--text-secondary);">Bạn gõ đúng <strong style="color:var(--color-primary); font-size:1.4rem;">${score} / ${words.length}</strong> từ.</p>
                    <button class="btn btn-primary" onclick="window.startReviewGame('spelling')">🔄 Làm lại</button>
                </div>
            `;
            return;
        }
        
        const currentWord = words[currentIndex];
        const cleanWord = currentWord.en.replace(/'/g, "\\'");
        
        container.innerHTML = `
            <div class="quiz-container" style="max-width: 480px;">
                <div style="display:flex; justify-content:space-between; margin-bottom:16px; color:var(--text-muted); font-weight:600;">
                    <div>Câu hỏi: <span style="color:var(--text-primary);">${currentIndex + 1} / ${words.length}</span></div>
                    <div>Điểm số: <span style="color:var(--color-primary);">${score}</span></div>
                </div>
                <div class="quiz-question" style="margin-bottom:24px; position:relative; display:flex; flex-direction:column; align-items:center; gap:8px;">
                    <div style="color:var(--text-muted); font-size:0.9rem; font-weight:500;">Nghĩa tiếng Việt:</div>
                    <div style="color:var(--text-primary); font-size:1.5rem; font-weight:800;">"${currentWord.vn}"</div>
                    <button class="btn-speak-vocab" onclick="window.speakWord('${cleanWord}')" style="margin-top:12px; width:40px; height:40px;" title="Nghe gợi ý phát âm">
                        <svg viewBox="0 0 24 24" width="18" height="18" fill="currentColor">
                            <path d="M12 3L6.5 8H2V16H6.5L12 21V3ZM16.5 12C16.5 10.23 15.48 8.71 14 8V16C15.48 15.29 16.5 13.77 16.5 12ZM14 3.23V5.29C16.89 6.15 19 8.83 19 12C19 15.17 16.89 17.85 14 18.71V20.77C18.01 19.86 21 16.28 21 12C21 7.72 18.01 4.14 14 3.23Z"/>
                        </svg>
                    </button>
                </div>
                <div style="display:flex; flex-direction:column; gap:12px; width:100%;">
                    <input type="text" id="spell-input" placeholder="Gõ từ tiếng Anh tương ứng..." autocomplete="off" spellcheck="false" 
                           style="width:100%; padding:14px 20px; font-size:1.15rem; border-radius:10px; border:2px solid var(--border-color); background:var(--bg-card); color:var(--text-primary); outline:none; transition:border-color 0.2s;">
                    <div id="spell-error" style="color:#ef4444; font-size:0.85rem; font-weight:600; display:none; text-align:center;">Chưa chính xác, thử lại nhé!</div>
                    <button class="btn btn-primary" id="spell-btn" style="width:100%; padding:12px; font-size:1.05rem; font-weight:700; background:linear-gradient(135deg, #ec4899, #be185d); border:none; color:white;">🔍 Kiểm tra</button>
                </div>
            </div>
        `;
        
        const input = document.getElementById('spell-input');
        const btn = document.getElementById('spell-btn');
        const errorText = document.getElementById('spell-error');
        
        setTimeout(() => input.focus(), 100);
        let attempts = 0;
        
        function checkAnswer() {
            const val = input.value.trim().toLowerCase();
            const correctVal = currentWord.en.split('/')[0].split(',')[0].replace(/\([^)]*\)/g, '').trim().toLowerCase();
            
            if (val === correctVal || val === currentWord.en.toLowerCase()) {
                sfx.correct();
                window.speakWord(currentWord.en);
                input.style.borderColor = '#22c55e';
                input.style.backgroundColor = 'rgba(34, 197, 94, 0.1)';
                input.style.color = '#166534';
                btn.disabled = true;
                if (attempts === 0) score++;
                
                setTimeout(() => {
                    currentIndex++;
                    renderSpelling();
                }, 1500);
            } else {
                sfx.wrong();
                attempts++;
                input.style.borderColor = '#ef4444';
                input.classList.add('error');
                errorText.style.display = 'block';
                input.value = '';
                
                if (attempts >= 3) {
                    errorText.innerHTML = `Gợi ý đáp án đúng: <strong style="color:var(--text-primary);">${currentWord.en}</strong>`;
                }
                
                setTimeout(() => {
                    input.classList.remove('error');
                }, 500);
            }
        }
        
        btn.onclick = checkAnswer;
        input.onkeypress = (e) => {
            if (e.key === 'Enter') checkAnswer();
        };
    }
    
    renderSpelling();
}

