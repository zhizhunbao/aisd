// ═══════════════════════════════════════════════════════════
// 公式图解注册表 — 按数学学科分类 (对齐 knowledge-map)
// Formula Diagram Registry — by math discipline
// ═══════════════════════════════════════════════════════════

import React from 'react'

// ── 微积分 (自定义 SVG) ──
import { DerivativeDiagram } from './DerivativeDiagram'
import { ChainRuleDiagram } from './ChainRuleDiagram'
import { SigmoidDiagram } from './SigmoidDiagram'
import { ReLUDiagram } from './ReLUDiagram'
import { TanhDiagram } from './TanhDiagram'
import { JacobianDiagram } from './JacobianDiagram'
import { HessianDiagram } from './HessianDiagram'
import { SoftplusDiagram } from './SoftplusDiagram'
import { LeakyReLUDiagram } from './LeakyReLUDiagram'
import { PartialDiagram, GradientDiagram } from './SimpleDiagrams'

// ── 线性代数 (自定义 SVG) ──
import { DotProductDiagram } from './DotProductDiagram'
import { MatMulDiagram } from './MatMulDiagram'
import { TransposeDiagram } from './TransposeDiagram'
import { EuclideanDiagram } from './EuclideanDiagram'
import { ManhattanDiagram } from './ManhattanDiagram'
import { CosineDiagram } from './CosineDiagram'
import { L1NormDiagram } from './L1NormDiagram'
import { DeterminantDiagram } from './DeterminantDiagram'
import { SVDDiagram } from './SVDDiagram'
import { NormalEquationDiagram } from './NormalEquationDiagram'
import { L2NormDiagram, EigenvalueDiagram } from './SimpleDiagrams'

// ── 概率论 (自定义 SVG) ──
import { BayesDiagram } from './BayesDiagram'
import { GaussianDiagram } from './GaussianDiagram'
import { SoftmaxDiagram } from './SoftmaxDiagram'
import { JointProbDiagram } from './JointProbDiagram'
import { TotalProbDiagram } from './TotalProbDiagram'
import { MultivariateGaussianDiagram } from './MultivariateGaussianDiagram'
import { MLEDiagram } from './MLEDiagram'
import { ConditionalDiagram, ExpectationDiagram } from './SimpleDiagrams'

// ── 数理统计 (自定义 SVG) ──
import { MSEDiagram } from './MSEDiagram'
import { CrossEntropyDiagram } from './CrossEntropyDiagram'
import { VarianceDiagram, MAEDiagram, MinkowskiDiagram } from './SimpleDiagrams'

// ── 优化方法 (自定义 SVG) ──
import { SGDDiagram } from './SGDDiagram'
import { MomentumDiagram, LearningRateDiagram } from './SimpleDiagrams'

// ── 信息论 ──
import { EntropyDiagram, KLDiagram } from './SimpleDiagrams'

// ── SimpleDiagrams2: 批量简单图解 ──
import {
  CovarianceDiagram, ZScoreDiagram,
  RMSPropDiagram, AdamDiagram, XavierInitDiagram, BatchNormDiagram,
  Conv1dDiagram, Conv2dDiagram, MultiHeadAttnDiagram, PosEncodingDiagram,
  ResidualDiagram, DropoutDiagram, LayerNormDiagram,
  RNNDiagram, LSTMDiagram, GRUDiagram,
  LinearRegressionDiagram, LogisticRegressionDiagram, SVMHingeDiagram,
  KernelRBFDiagram, KMeansDiagram, PCADiagram, NaiveBayesDiagram,
  InfoGainDiagram, GiniDiagram,
  L2RegDiagram, L1RegDiagram, ElasticNetDiagram,
  BCELossDiagram, FocalLossDiagram, TripletLossDiagram, ContrastiveLossDiagram,
  HuberLossDiagram, GANLossDiagram, VAEELBODiagram,
  AccuracyDiagram, PrecisionDiagram, RecallDiagram, F1Diagram, IoUDiagram,
  RSquaredDiagram, BiasVarianceDiagram,
  BernoulliDiagram, BinomialDiagram, PoissonDiagram, UniformDiagram,
  ExponentialDiagram, BetaDiagram, CategoricalDiagram,
  ExponentRulesDiagram, LogRulesDiagram, ChangeOfBaseDiagram, ExpLogInverseDiagram,
  QuadraticDiagram, BinomialTheoremDiagram, CombinationDiagram, FactorialDiagram,
  ArithSeriesDiagram, GeomSeriesDiagram, TaylorDiagram, EulerFormulaDiagram,
  PythagoreanDiagram, TrigBasicDiagram, SumProductDiagram, AbsValueDiagram,
  FloorCeilDiagram, MaxMinDiagram, SetOpsDiagram,
  MutualInfoDiagram, ConditionalEntropyDiagram, JointEntropyDiagram,
  TraceDiagram, FrobeniusDiagram, HadamardDiagram, OuterProductDiagram, PseudoInverseDiagram,
} from './SimpleDiagrams2'

const DIAGRAM_MAP: Record<string, React.FC<{ compact?: boolean }>> = {
  // ── 微积分 ──
  'fml-derivative':     DerivativeDiagram,
  'fml-partial':        PartialDiagram,
  'fml-gradient':       GradientDiagram,
  'fml-jacobian':       JacobianDiagram,
  'fml-hessian':        HessianDiagram,
  'fml-chain-rule':     ChainRuleDiagram,
  'fml-sigmoid':        SigmoidDiagram,
  'fml-tanh':           TanhDiagram,
  'fml-relu':           ReLUDiagram,
  'fml-softplus':       SoftplusDiagram,
  'fml-leaky-relu':     LeakyReLUDiagram,

  // ── 线性代数 ──
  'fml-l1-norm':        L1NormDiagram,
  'fml-l2-norm':        L2NormDiagram,
  'fml-dot-product':    DotProductDiagram,
  'fml-matrix-multiply': MatMulDiagram,
  'fml-transpose':      TransposeDiagram,
  'fml-determinant':    DeterminantDiagram,
  'fml-eigenvalue':     EigenvalueDiagram,
  'fml-svd':            SVDDiagram,
  'fml-normal-equation': NormalEquationDiagram,
  'fml-euclidean':      EuclideanDiagram,
  'fml-manhattan':      ManhattanDiagram,
  'fml-cosine':         CosineDiagram,
  'fml-trace':          TraceDiagram,
  'fml-frobenius':      FrobeniusDiagram,
  'fml-hadamard':       HadamardDiagram,
  'fml-outer-product':  OuterProductDiagram,
  'fml-pseudo-inverse': PseudoInverseDiagram,

  // ── 概率论 ──
  'fml-joint-prob':     JointProbDiagram,
  'fml-conditional':    ConditionalDiagram,
  'fml-total-prob':     TotalProbDiagram,
  'fml-bayes':          BayesDiagram,
  'fml-expectation':    ExpectationDiagram,
  'fml-gaussian':       GaussianDiagram,
  'fml-multivariate-gaussian': MultivariateGaussianDiagram,
  'fml-mle':            MLEDiagram,
  'fml-softmax':        SoftmaxDiagram,

  // ── 数理统计 ──
  'fml-variance':       VarianceDiagram,
  'fml-covariance':     CovarianceDiagram,
  'fml-zscore':         ZScoreDiagram,
  'fml-mae':            MAEDiagram,
  'fml-mse':            MSEDiagram,
  'fml-minkowski':      MinkowskiDiagram,

  // ── 优化方法 ──
  'fml-sgd':            SGDDiagram,
  'fml-momentum':       MomentumDiagram,
  'fml-learning-rate':  LearningRateDiagram,
  'fml-rmsprop':        RMSPropDiagram,
  'fml-adam':           AdamDiagram,
  'fml-xavier-init':    XavierInitDiagram,
  'fml-batchnorm':      BatchNormDiagram,

  // ── 信息论 ──
  'fml-entropy':        EntropyDiagram,
  'fml-cross-entropy':  CrossEntropyDiagram,
  'fml-kl-divergence':  KLDiagram,
  'fml-mutual-info':    MutualInfoDiagram,
  'fml-conditional-entropy': ConditionalEntropyDiagram,
  'fml-joint-entropy':  JointEntropyDiagram,

  // ── 深度学习 ──
  'fml-conv1d':         Conv1dDiagram,
  'fml-conv2d':         Conv2dDiagram,
  'fml-attention':      MultiHeadAttnDiagram,  // Scaled Dot-Product 复用
  'fml-multihead-attn': MultiHeadAttnDiagram,
  'fml-pos-encoding':   PosEncodingDiagram,
  'fml-residual':       ResidualDiagram,
  'fml-dropout':        DropoutDiagram,
  'fml-layernorm':      LayerNormDiagram,

  // ── 序列模型 ──
  'fml-rnn':            RNNDiagram,
  'fml-lstm':           LSTMDiagram,
  'fml-gru':            GRUDiagram,

  // ── ML 算法 ──
  'fml-linear-regression':   LinearRegressionDiagram,
  'fml-logistic-regression': LogisticRegressionDiagram,
  'fml-svm-hinge':      SVMHingeDiagram,
  'fml-kernel-rbf':     KernelRBFDiagram,
  'fml-kmeans':         KMeansDiagram,
  'fml-pca':            PCADiagram,
  'fml-naive-bayes':    NaiveBayesDiagram,
  'fml-info-gain':      InfoGainDiagram,
  'fml-gini':           GiniDiagram,

  // ── 正则化 ──
  'fml-l2-reg':         L2RegDiagram,
  'fml-l1-reg':         L1RegDiagram,
  'fml-elastic-net':    ElasticNetDiagram,

  // ── 损失函数 ──
  'fml-bce-loss':       BCELossDiagram,
  'fml-focal-loss':     FocalLossDiagram,
  'fml-triplet-loss':   TripletLossDiagram,
  'fml-contrastive-loss': ContrastiveLossDiagram,
  'fml-huber-loss':     HuberLossDiagram,
  'fml-gan-loss':       GANLossDiagram,
  'fml-vae-elbo':       VAEELBODiagram,

  // ── 评估指标 ──
  'fml-accuracy':       AccuracyDiagram,
  'fml-precision':      PrecisionDiagram,
  'fml-recall':         RecallDiagram,
  'fml-f1':             F1Diagram,
  'fml-iou':            IoUDiagram,
  'fml-r-squared':      RSquaredDiagram,
  'fml-bias-variance':  BiasVarianceDiagram,

  // ── 概率分布 ──
  'fml-bernoulli':      BernoulliDiagram,
  'fml-binomial':       BinomialDiagram,
  'fml-poisson':        PoissonDiagram,
  'fml-uniform':        UniformDiagram,
  'fml-exponential':    ExponentialDiagram,
  'fml-beta':           BetaDiagram,
  'fml-categorical':    CategoricalDiagram,

  // ── 基础数学 ──
  'fml-exponent-rules': ExponentRulesDiagram,
  'fml-log-rules':      LogRulesDiagram,
  'fml-change-of-base': ChangeOfBaseDiagram,
  'fml-exp-log-inverse': ExpLogInverseDiagram,
  'fml-quadratic':      QuadraticDiagram,
  'fml-binomial-theorem': BinomialTheoremDiagram,
  'fml-combination':    CombinationDiagram,
  'fml-factorial':      FactorialDiagram,
  'fml-arithmetic-series': ArithSeriesDiagram,
  'fml-geometric-series': GeomSeriesDiagram,
  'fml-taylor':         TaylorDiagram,
  'fml-euler-formula':  EulerFormulaDiagram,
  'fml-pythagorean':    PythagoreanDiagram,
  'fml-trig-sin-cos':   TrigBasicDiagram,
  'fml-sum-product':    SumProductDiagram,
  'fml-abs-value':      AbsValueDiagram,
  'fml-floor-ceil':     FloorCeilDiagram,
  'fml-max-min':        MaxMinDiagram,
  'fml-set-ops':        SetOpsDiagram,
}

export function getDiagramComponent(formulaId: string): React.FC<{ compact?: boolean }> | undefined {
  return DIAGRAM_MAP[formulaId]
}

export function FormulaDiagram({ formulaId, compact }: { formulaId: string; compact?: boolean }) {
  const Diagram = DIAGRAM_MAP[formulaId]
  if (!Diagram) return null
  return <Diagram compact={compact} />
}
